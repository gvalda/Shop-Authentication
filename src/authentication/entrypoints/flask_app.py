from flask import Flask, request, jsonify

from authentication.exceptions import(
    RegistrationError,
    AuthenticationError,
    VerificationError,
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
    except RegistrationError as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return 'Created', HttpStatusCodes.CREATED_201


@app.route('/auth/token', methods=['POST'])
def login():
    try:
        cmd = commands.LoginUser(
            request.json['username'],
            request.json['password'],
        )
        results = bus.handle(cmd)
        tokens = results.pop(0)
    except AuthenticationError as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return jsonify(tokens), HttpStatusCodes.OK_200


@app.route('/auth/token/refresh', methods=['POST'])
def refresh():
    try:
        cmd = commands.RefreshToken(
            request.json['token'],
        )
        results = bus.handle(cmd)
        tokens = results.pop(0)
    except AuthenticationError as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return jsonify(tokens), HttpStatusCodes.OK_200


@app.route('/auth/email/verify', methods=['POST'])
def verify():
    try:
        cmd = commands.VerifyUserEmail(
            request.json['token'],
        )
        bus.handle(cmd)
    except VerificationError as e:
        return {'message': str(e)}, HttpStatusCodes.BAD_REQUEST_400
    return 'Verified', HttpStatusCodes.OK_200
