from flask import Flask
from flask import request, jsonify, Response
import requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)


account_id = 1

ratings = [
    {'account_id': 1, 'rating': 5, 'book_id': 2},
    {'account_id': 2, 'rating': 3, 'book_id': 2},
    {'account_id': 1, 'rating': 1, 'book_id': 1}
]

@app.route("/ratings/", methods=['GET'])
def rating_list():
    account_rating = {item for item in ratings if item.get('account_id') == account_id}
    with tracer.start_as_current_span("rating_list"):
        requests.get("/books/")
    return jsonify()
