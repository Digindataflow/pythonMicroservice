from flask import Flask
from flask import request, jsonify, Response
from datetime import datetime
from books.domain import commands
from books.service_layer.handlers import InvalidIsbn
from books import bootstrap
from books import views
import os

app = Flask(__name__)
bus = bootstrap.bootstrap()

@app.route("/books/", methods=['GET'])
def book_list():
    isbns = request.args.to_dict(flat=False).get('isbn')
    result = views.books(isbns, bus.uow)
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
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    print(host, port)
    app.run(host=host, port=port, debug=True)