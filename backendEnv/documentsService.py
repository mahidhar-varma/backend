from unicodedata import category
from importlib_metadata import method_cache
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.dbModels import documentModel, db
from flasgger import swag_from
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.app = app
db.init_app(app)

# db.create_all()
# documents = Blueprint("documents", __name__, url_prefix="/api/v1/documents")

#get, post, put, delete
# at /documents/category/
# allowed add a document, get documents, delete all documents

# at /documents/category/<docID>
# allowed add a document
# get document, modify and delete a document


@app.route('/<string:category>', methods=['POST', 'GET', 'DELETE'])
# @jwt_required()
def handle_documents(category):
    # current_user = get_jwt_identity()

    if request.method == 'POST':

        userId = request.get_json().get('userId', '')
        documentName = request.get_json().get('documentName', '')
        doctorName = request.get_json().get('documentName', '')
        hospitalName = request.get_json().get('hospitalName', '')
        issuedDate = request.get_json().get('issuedDate', '')
        documentURL = "testurl"

        if documentModel.query.filter_by(category=category, documentName=documentName).first():
            return jsonify({
                'error': 'A document with the same name exists!!'
            }), HTTP_409_CONFLICT

        document = documentModel(userId=userId, category=category, documentName=documentName,
                                 doctorName=doctorName, hospitalName=hospitalName, issuedDate=issuedDate, documentURL=documentURL)
        db.session.add(document)
        db.session.commit()

        return jsonify({
            'documentid': document.documentId,
            'category': document.category,
            'documentName': document.documentName,
            'doctorName': document.doctorName,
            'hospitalName': document.hospitalName,
            'documentURL': document.documentURL,
            'issuedDate': document.issuedDate,
        }), HTTP_201_CREATED

    if request.method == 'GET':

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        documents = documentModel.query.filter_by(
            category=category).paginate(page=page, per_page=per_page)

        data = []

        for document in documents.items:
            data.append({
                'documentid': document.documentId,
                'category': document.category,
                'documentName': document.documentName,
                'doctorName': document.doctorName,
                'hospitalName': document.hospitalName,
                'documentURL': document.documentURL,
                'issuedDate': document.issuedDate
            })

        return jsonify({'data': data}), HTTP_200_OK

    if request.method == 'DELETE':

        documents = documentModel.query.filter_by(
            category=category)

        for document in documents:
            db.session.delete(document)
            db.session.commit()

        return jsonify({}), HTTP_204_NO_CONTENT


@app.route('/<string:category>/<string:documentId>', methods=['POST', 'GET', 'PATCH', 'DELETE', 'PUT'])
def handle_document(category, documentId):
    if request.method == 'GET':
        # current_user = get_jwt_identity()
        print("inside get")
        document = documentModel.query.filter_by(
            documentId=documentId, category=category).first()
        print("inside get0")
        if not document:
            return jsonify({'message': 'Document not found'}), HTTP_404_NOT_FOUND
        print("inside get1")
        return jsonify({
            'documentId': document.documentId,
            'category': document.category,
            'documentName': document.documentName,
            'doctorName': document.doctorName,
            'hospitalName': document.hospitalName,
            'documentURL': document.documentURL,
            'issuedDate': document.issuedDate
        }), HTTP_200_OK

    elif request.method == "DELETE":
        # current_user = get_jwt_identity()

        document = documentModel.query.filter_by(
            documentId=documentId, category=category).first()

        if not document:
            return jsonify({'message': 'Document not found'}), HTTP_404_NOT_FOUND

        db.session.delete(document)
        db.session.commit()

        return jsonify({}), HTTP_204_NO_CONTENT

    elif request.method == "PUT" or request.method == "PATCH":
        # current_user = get_jwt_identity()

        document = documentModel.query.filter_by(
            documentId=documentId, category=category).first()

        if not document:
            return jsonify({'message': 'Document not found'}), HTTP_404_NOT_FOUND

        userId = request.get_json().get('userId', '')
        documentName = request.get_json().get('documentName', '')
        doctorName = request.get_json().get('documentName', '')
        hospitalName = request.get_json().get('hospitalName', '')
        issuedDate = request.get_json().get('issuedDate', '')
        documentURL = "testurl"

        if documentName:
            document.documentName = documentName
        if doctorName:
            document.doctorName = doctorName
        if hospitalName:
            document.hospitalName = hospitalName
        if issuedDate:
            document.issuedDate = issuedDate

        db.session.commit()

        return jsonify({
            'documentid': document.documentId,
            'category': document.category,
            'documentName': document.documentName,
            'doctorName': document.doctorName,
            'hospitalName': document.hospitalName,
            'documentURL': document.documentURL,
            'issuedDate': document.issuedDate
        }), HTTP_200_OK


categories = ["Prescription", "Lab-Reports"]


@app.get("/<string:userId>/stats")
# @jwt_required()
def get_stats(userId):
    # current_user = get_jwt_identity()
    data = {}
    print('userId:   ', userId)
    for cCategory in categories:
        cCount = documentModel.query.filter_by(
            userId=userId, category=cCategory).count()
        data[cCategory] = cCount
    return jsonify(data), HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=True)
