from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import LoggedRoutineSet, db
#import src.constants.http_status_codes

logged_routine_sets = Blueprint("logged_routine_sets", __name__, url_prefix="/api/logged_routine_sets")

@logged_routine_sets.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'logged routine sets test'}), 200)

# Get all logged routine sets
@logged_routine_sets.route('/', methods=['GET'])
def get_logged_routine_sets():
    try:
        logged_routine_sets = LoggedRoutineSet.query.all()
        return make_response(jsonify([logged_routine_set.json() for logged_routine_set in logged_routine_sets]), 200)
    except:
        return make_response(jsonify({'message': 'error getting logged routine sets'}), 500)

# Create a logged routine set
@logged_routine_sets.route('/', methods=['POST'])
def create_logged_routine_set():
    try:
        data = request.get_json()
        new_logged_routine_set = LoggedRoutineSet(
            loggedRoutineId=data['loggedRoutineId'],
            exerciseId=data['exerciseId'],
            exerciseName=data['exerciseName'],
            warmupSetsCount=data['warmupSetsCount'],
            setsCount=data['setsCount'],
            setsOrder=data['setsOrder'],
            userUID=data['userUID']
        )

        db.session.add(new_logged_routine_set)
        db.session.commit()
        return make_response(jsonify({'message': 'logged routine set created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating logged routine set'}), 500)

# Update a logged routine set
@logged_routine_sets.route('/<int:loggedRoutineSetId>', methods=['PUT'])
def update_logged_routine_set(loggedRoutineSetId):
    try:
        logged_routine_set = LoggedRoutineSet.query.filter_by(loggedRoutineSetId=loggedRoutineSetId).first()
        if logged_routine_set:
            data = request.get_json()

            logged_routine_set.loggedRoutineId = data['loggedRoutineId']
            logged_routine_set.exerciseId = data['exerciseId']
            logged_routine_set.exerciseName = data['exerciseName']
            logged_routine_set.warmupSetsCount = data['warmupSetsCount']
            logged_routine_set.setsCount = data['setsCount']
            logged_routine_set.setsOrder = data['setsOrder']
            logged_routine_set.userUID = data['userUID']

            db.session.commit()
            return make_response(jsonify({'message': 'logged routine set updated'}), 200)
        return make_response(jsonify({'message': 'logged routine set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating logged routine set'}), 500)

# Delete a logged routine set
@logged_routine_sets.route('/<int:loggedRoutineSetId>', methods=['DELETE'])
def delete_logged_routine_set(loggedRoutineSetId):
    try:
        logged_routine_set = LoggedRoutineSet.query.filter_by(loggedRoutineSetId=loggedRoutineSetId).first()
        if logged_routine_set:
            db.session.delete(logged_routine_set)
            db.session.commit()
            return make_response(jsonify({'message': 'logged routine set deleted'}), 200)
        return make_response(jsonify({'message': 'logged routine set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting logged routine set'}), 500)
