from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import RoutineSet, db
#import src.constants.http_status_codes

routine_sets = Blueprint("routine_sets", __name__, url_prefix="/api/routine_sets")

@routine_sets.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'routine sets test'}), 200)

# Get all routine sets
@routine_sets.route('/', methods=['GET'])
def get_routine_sets():
    try:
        routine_sets = RoutineSet.query.all()
        return make_response(jsonify([routine_set.json() for routine_set in routine_sets]), 200)
    except:
        return make_response(jsonify({'message': 'error getting routine sets'}), 500)

# Create a routine set
@routine_sets.route('/', methods=['POST'])
def create_routine_set():
    try:
        data = request.get_json()
        new_routine_set = RoutineSet(
            routineId=data['routineId'],
            exerciseId=data['exerciseId'],
            warmupSetsCount=data['warmupSetsCount'],
            setsCount=data['setsCount'],
            setsOrder=data['setsOrder'],
            isUserMade=data['isUserMade'],
            userUID=data['userUID']
        )

        db.session.add(new_routine_set)
        db.session.commit()
        return make_response(jsonify({'message': 'routine set created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating routine set'}), 500)

# Update a routine set
@routine_sets.route('/<int:routineSetId>', methods=['PUT'])
def update_routine_set(routineSetId):
    try:
        routine_set = RoutineSet.query.filter_by(routineSetId=routineSetId).first()
        if routine_set:
            data = request.get_json()

            routine_set.routineId = data['routineId']
            routine_set.exerciseId = data['exerciseId']
            routine_set.warmupSetsCount = data['warmupSetsCount']
            routine_set.setsCount = data['setsCount']
            routine_set.setsOrder = data['setsOrder']
            routine_set.isUserMade = data['isUserMade']
            routine_set.userUID = data['userUID']

            db.session.commit()
            return make_response(jsonify({'message': 'routine set updated'}), 200)
        return make_response(jsonify({'message': 'routine set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating routine set'}), 500)

# Delete a routine set
@routine_sets.route('/<int:routineSetId>', methods=['DELETE'])
def delete_routine_set(routineSetId):
    try:
        routine_set = RoutineSet.query.filter_by(routineSetId=routineSetId).first()
        if routine_set:
            db.session.delete(routine_set)
            db.session.commit()
            return make_response(jsonify({'message': 'routine set deleted'}), 200)
        return make_response(jsonify({'message': 'routine set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting routine set'}), 500)
