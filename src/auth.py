import json
from flask import Blueprint, jsonify,request
import validators
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST,HTTP_200_OK

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        email = request.json['email']
        dob = request.json['dob']
        mobile_no = request.json['mobile_no']
        gender = request.json['gender']

        if not validators.email(email):
            return jsonify({'error':"Email is not valid"}), HTTP_400_BAD_REQUEST

    return jsonify({'auth':"{}"}), HTTP_200_OK

@auth.get("/me")
def index():
    return jsonify({'auth':"Auth"}), HTTP_200_OK