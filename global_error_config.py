from flask import jsonify, Response
from sqlalchemy.exc import IntegrityError, DataError

from flaskr import app
from flaskr.exceptions.auth_exception import AuthError
from flaskr.exceptions.functional_exception import FunctionalException
from flaskr.exceptions.not_found_exception import NotFound


@app.errorhandler(NotFound)
def handle_auth_error(ex: NotFound) -> Response:
    response = jsonify(ex.error)
    response.status_code = ex.status_code

    return response


@app.errorhandler(IntegrityError)
def handle_integrity_error(err: IntegrityError) -> Response:
    response = jsonify({
        "code": 403,
        "description": "Operation violates foreign key contraint"
    })

    return response, 403

@app.errorhandler(DataError)
def handle_data_error(err: DataError) -> Response:
    response = jsonify({
        "code": 403,
        "description": "Data sent to save is not valid"
    })

    return response, 403


@app.errorhandler(FunctionalException)
def handle_sql_error(ex: IntegrityError) -> Response:
    response = jsonify(ex.error)
    response.status_code = ex.status_code

    return response


@app.errorhandler(AuthError)
def handle_auth_error(ex: AuthError) -> Response:
    response = jsonify(ex.error)
    response.status_code = ex.status_code

    return response
