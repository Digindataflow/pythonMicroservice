from flask import Flask
from flask import request, jsonify, Response

app = Flask(__name__)
books = [
    {'id': 1, 'name': 'book1'},
    {'id': 2, 'name': 'book2'},
    {'id': 3, 'name': 'book3'}
]

@app.route("/books/", methods=['GET', 'POST'])
def book_list():
    if request.method == 'GET':
        book_ids = request.args.to_dict(flat=False).get('id')
        book_ids = [int(item) for item in book_ids]
        if book_ids:
            items = [item for item in books if item['id'] in book_ids]
        else:
            items = books
        return jsonify(items)
    else:
        book = request.get_json()
        books.append(book)
        return Response(status=201)