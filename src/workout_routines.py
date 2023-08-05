from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import WorkoutRoutine, db
#import src.constants.http_status_codes

workout_routines = Blueprint("workout_routines", __name__, url_prefix="/api/workout_routines")

@workout_routines.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'workout routines test'}), 200)

# Get all workout routines
@workout_routines.route('/', methods=['GET'])
def get_workout_routines():
    try:
        workout_routines = WorkoutRoutine.query.all()
        return make_response(jsonify([routine.json() for routine in workout_routines]), 200)
    except:
        return make_response(jsonify({'message': 'error getting workout routines'}), 500)

# Create a workout routine
@workout_routines.route('/', methods=['POST'])
def create_workout_routine():
    try:
        data = request.get_json()
        new_routine = WorkoutRoutine(
            name=data['name'],
            notes=data['notes'],
            isUserMade=data['isUserMade'],
            userUID=data['userUID']
        )

        db.session.add(new_routine)
        db.session.commit()
        return make_response(jsonify({'message': 'workout routine created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating workout routine'}), 500)

# Update a workout routine
@workout_routines.route('/<int:routineId>', methods=['PUT'])
def update_workout_routine(routineId):
    try:
        routine = WorkoutRoutine.query.filter_by(routineId=routineId).first()
        if routine:
            data = request.get_json()

            routine.name = data['name']
            routine.notes = data['notes']
            routine.isUserMade = data['isUserMade']
            routine.userUID = data['userUID']

            db.session.commit()
            return make_response(jsonify({'message': 'workout routine updated'}), 200)
        return make_response(jsonify({'message': 'workout routine not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating workout routine'}), 500)

# Delete a workout routine
@workout_routines.route('/<int:routineId>', methods=['DELETE'])
def delete_workout_routine(routineId):
    try:
        routine = WorkoutRoutine.query.filter_by(routineId=routineId).first()
        if routine:
            db.session.delete(routine)
            db.session.commit()
            return make_response(jsonify({'message': 'workout routine deleted'}), 200)
        return make_response(jsonify({'message': 'workout routine not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting workout routine'}), 500)
