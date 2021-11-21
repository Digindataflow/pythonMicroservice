import os
from datetime import datetime

from flask import Flask, Response, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from books import bootstrap, views
from books.domain import commands
from books.service_layer.handlers import InvalidIsbn

app = Flask(__name__)
bus = bootstrap.bootstrap()
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'books', version='1.0.0')

@app.route("/books/", methods=['GET'])
def book_list():
    isbns = request.args.to_dict(flat=False).get('isbn')
    result = views.books(isbns, bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200


@app.route("/books/<isbn>", methods=['GET'])
def get_book(isbn: str):
    result = views.books([isbn], bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200


@app.route("/books/", methods=["POST"])
def add_book():
    pub_date = request.json.get("pub_date")
    if pub_date is not None:
        pub_date = datetime.fromisoformat(pub_date).date()

    try:
        cmd = commands.AddBook(
            request.json["isbn"], request.json["name"], request.json["price"], pub_date
        )
        bus.handle(cmd)
    except InvalidIsbn as e:
        return {"message": str(e)}, 400

    return "OK", 201

if __name__ == "__main__":
    from .config import get_api_url
    host_port = get_api_url()
    print(host_port)
    # app.run(host_port.get("host"), host_port.get("port"), debug=True)
    # Plug metrics WSGI app to your main app with dispatcher
    dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    run_simple(hostname=host_port.get("host"), port=host_port.get("port"), application=dispatcher)