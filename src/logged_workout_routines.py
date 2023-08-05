from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import LoggedWorkoutRoutine, db
import datetime
#import src.constants.http_status_codes

logged_workout_routines = Blueprint("logged_workout_routines", __name__, url_prefix="/api/logged_workout_routines")

@logged_workout_routines.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'logged workout routines test'}), 200)

# Get all logged workout routines
@logged_workout_routines.route('/', methods=['GET'])
def get_logged_workout_routines():
    try:
        logged_workout_routines = LoggedWorkoutRoutine.query.all()
        return make_response(jsonify([routine.json() for routine in logged_workout_routines]), 200)
    except:
        return make_response(jsonify({'message': 'error getting logged workout routines'}), 500)

# Create a logged workout routine
@logged_workout_routines.route('/', methods=['POST'])
def create_logged_workout_routine():
    try:
        data = request.get_json()
        new_routine = LoggedWorkoutRoutine(
            name=data['name'],
            bodyweight=data['bodyweight'],
            notes=data['notes'],
            date=datetime.datetime.strptime(data['date'], "%Y-%m-%d").date(),
            startTime=datetime.datetime.strptime(data['startTime'], "%H:%M:%S").time(),
            endTime=datetime.datetime.strptime(data['endTime'], "%H:%M:%S").time() if 'endTime' in data else None,
            userUID=data['userUID']
        )

        db.session.add(new_routine)
        db.session.commit()
        return make_response(jsonify({'message': 'logged workout routine created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating logged workout routine'}), 500)

# Update a logged workout routine
@logged_workout_routines.route('/<int:loggedRoutineId>', methods=['PUT'])
def update_logged_workout_routine(loggedRoutineId):
    try:
        routine = LoggedWorkoutRoutine.query.filter_by(loggedRoutineId=loggedRoutineId).first()
        if routine:
            data = request.get_json()

            routine.name = data['name']
            routine.bodyweight = data['bodyweight']
            routine.notes = data['notes']
            routine.date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
            routine.startTime = datetime.datetime.strptime(data['startTime'], "%H:%M:%S").time()
            routine.endTime = datetime.datetime.strptime(data['endTime'], "%H:%M:%S").time() if 'endTime' in data else None
            routine.userUID = data['userUID']

            db.session.commit()
            return make_response(jsonify({'message': 'logged workout routine updated'}), 200)
        return make_response(jsonify({'message': 'logged workout routine not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating logged workout routine'}), 500)

# Delete a logged workout routine
@logged_workout_routines.route('/<int:loggedRoutineId>', methods=['DELETE'])
def delete_logged_workout_routine(loggedRoutineId):
    try:
        routine = LoggedWorkoutRoutine.query.filter_by(loggedRoutineId=loggedRoutineId).first()
        if routine:
            db.session.delete(routine)
            db.session.commit()
            return make_response(jsonify({'message': 'logged workout routine deleted'}), 200)
        return make_response(jsonify({'message': 'logged workout routine not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting logged workout routine'}), 500)
