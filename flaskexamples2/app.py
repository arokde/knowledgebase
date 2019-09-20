import jwt
from datetime import datetime, timedelta
from flask import jsonify, request, Response
from functools import wraps

from BookModel import *
from UserModel import *

books = [
    {"name": "Welcome to python basic", "price": 7.99, "isbn": 98888},
    {"name": "Welcome to python advanced", "price": 10.99, "isbn": 98688},
]

app.config['SECRET_KEY'] = 'test'


def token_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.headers.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args,**kwargs)
        except:
            return jsonify({'error': 'Need a valid token for request'}), 401
    return wrapper;


@app.route('/login',methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data["username"])
    password = str(request_data["password"])
    if not User.username_password_match(username,password):
        return Response('',401,mimetype='application/json')
    expiration_date = datetime.utcnow() + timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date},app.config['SECRET_KEY'],algorithm='HS256')
    return token

def valid_book_object(book_object):
    if "name" in book_object and "price" in book_object and "isbn" in book_object:
        return True
    else:
        return False


@app.route("/books")
def get_all_books():
    return jsonify({"books": Book.get_all_books()})


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        Book.add_book(request_data["name"],request_data["price"],request_data["isbn"])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data["isbn"])
        return response
    else:
        invalid_error_object_error_msg = {
            "error":"Invalid book object passed in the request",
            "helpString":"Data passed in similar to this {'name':'bookname','price': 20, 'isbn':8888}"
        }
        response = Response(json.dumps(invalid_error_object_error_msg), 400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}

#    for book in books:
#        if book["isbn"] == isbn:
#           return_value = {
#               'name': book["name"],
#               'price': book["price"]
#            }
#            break
    return jsonify(Book.get_book(isbn))


@app.route('/books/<int:isbn>', methods=["PUT"])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_book_object(request_data):
        invalid_error_object_error_msg = {
            "error": "Invalid book object passed in the request",
            "helpString": "Data passed in similar to this {'name':'bookname','price': 20, 'isbn':8888}"
        }
        response = Response(json.dumps(invalid_error_object_error_msg), 400, mimetype='application/json')
        return response
    Book.replace_book(isbn,request_data["name"],request_data["price"])
    response  = Response("",status=204)
    return response


@app.route('/books/<int:isbn>/<nameoffield>', methods=['PATCH'])
@token_required
def update_book(isbn,nameoffield):
    request_data = request.get_json()
    local_update_book = {}
    if nameoffield == "name":
        Book.update_book_name(isbn,request_data[nameoffield])
    elif nameoffield == "price":
        Book.update_book_price(isbn, request_data[nameoffield])
    response = Response("",status=204)
    response.headers["Location"] = '/books/' + str(isbn)
    return response


@app.route('/books/<int:isbn>',methods=['DELETE'])
@token_required
def delete_book(isbn):

    if Book.delete_book(isbn):
        response = Response("", status=200)
    else:
        invalid_error_object_error_msg = {
        "error": "Object with id " + str(isbn) + " not found",
        }
        response = Response(json.dumps(invalid_error_object_error_msg), 404, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run()
