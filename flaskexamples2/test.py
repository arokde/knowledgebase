from app import valid_book_object

valid_object = {
    'name': 'F',
    'price': 6.99,
    'isbn': 123444
}

missing_name = {
    'price': 6.99,
    'isbn': 12233
}

missing_price = {
    'name': 'name',
    'isbn': 2233
}

empty_object = {}


def test_valid_object():
    assert valid_book_object(valid_object) == True


def test_missing_name():
    assert valid_book_object(missing_name) == False


def test_missing_price():
    assert valid_book_object(missing_price) == False


def test_empty_object():
    assert valid_book_object(empty_object) == False
