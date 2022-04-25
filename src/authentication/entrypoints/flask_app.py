from flask import Flask, request, jsonify

from authentication.exceptions import(
    InvalidUserCredentials,
    UserAlreadyExists,
    UserNotVerified,
    UserDeleted,
    UserBanned,
    InvalidToken,
)
from authentication.domain import commands, events
from authentication.bootstrap import bootstrap
from authentication.enums import HttpStatusCodes

app = Flask(__name__)
bus = bootstrap()

# TODO add logging


@app.route('/auth/register', methods=['POST'])
def register():
    try:
        cmd = commands.CreateUser(
            request.json['username'],
            request.json['password'],
            request.json['email'],
        )
        bus.handle(cmd)
    except UserAlreadyExists as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return 'Created', HttpStatusCodes.CREATED_201


@app.route('/auth/login', methods=['POST'])
def login():
    try:
        cmd = commands.LoginUser(
            request.json['username'],
            request.json['password'],
        )
        results = bus.handle(cmd)
        tokens = results.pop(0)
    except (
        InvalidUserCredentials,
        UserBanned,
        UserDeleted,
        UserNotVerified,
    ) as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400

    return jsonify(tokens), HttpStatusCodes.OK_200


@app.route('/auth/verify', methods=['GET'])
def get_user_email_verification():
    pass


@app.route('/auth/verify/<token>', methods=['POST'])
def verify_user_email(token):
    try:
        cmd = commands.VerifyUserEmail(token)
        bus.handle(cmd)
    except InvalidToken as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return 'Verified', HttpStatusCodes.OK_200
