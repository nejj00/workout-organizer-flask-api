from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import User, db
import datetime
#import src.constants.http_status_codes

users = Blueprint("users", __name__, url_prefix="/api/users")

@users.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'users test'}), 200)

# Get all users
@users.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except:
        return make_response(jsonify({'message': 'error getting users'}), 500)

# Create a user
@users.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            userUID=data['userUID'],
            email=data['email'],
            bodyweight=data['bodyweight'],
            userCreated=datetime.datetime.strptime(data['userCreated'], "%Y-%m-%d").date(),
            userLastLogin=datetime.datetime.strptime(data['userLastLogin'], "%Y-%m-%d").date(),
        )

        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating user'}), 500)

# Update a user
@users.route('/<int:userId>', methods=['PUT'])
def update_user(userId):
    try:
        user = User.query.filter_by(userId=userId).first()
        if user:
            data = request.get_json()

            user.userUID = data['userUID']
            user.email = data['email']
            user.bodyweight = data['bodyweight']
            user.userCreated = datetime.datetime.strptime(data['userCreated'], "%Y-%m-%d").date()
            user.userLastLogin = datetime.datetime.strptime(data['userLastLogin'], "%Y-%m-%d").date()
            
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating user'}), 500)

# Delete a user
@users.route('/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    try:
        user = User.query.filter_by(userId=userId).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting user'}), 500)
