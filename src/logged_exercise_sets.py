from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import LoggedExerciseSet, db
#import src.constants.http_status_codes

logged_exercise_sets = Blueprint("logged_exercise_sets", __name__, url_prefix="/api/logged_exercise_sets")

@logged_exercise_sets.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'logged exercise sets test'}), 200)

# Get all logged exercise sets
@logged_exercise_sets.route('/', methods=['GET'])
def get_logged_exercise_sets():
    try:
        logged_exercise_sets = LoggedExerciseSet.query.all()
        return make_response(jsonify([logged_exercise_set.json() for logged_exercise_set in logged_exercise_sets]), 200)
    except:
        return make_response(jsonify({'message': 'error getting logged exercise sets'}), 500)

# Create a logged exercise set
@logged_exercise_sets.route('/', methods=['POST'])
def create_logged_exercise_set():
    try:
        data = request.get_json()
        new_logged_exercise_set = LoggedExerciseSet(
            loggedRoutineId=data['loggedRoutineId'],
            loggedRoutineSetId=data['loggedRoutineSetId'],
            weight=data['weight'],
            reps=data['reps'],
            setOrder=data['setOrder'],
            isWarmupSet=data['isWarmupSet'],
            notes=data['notes'],
            userUID=data['userUID']
        )

        db.session.add(new_logged_exercise_set)
        db.session.commit()
        return make_response(jsonify({'message': 'logged exercise set created'}), 201)
    except:
        return make_response(jsonify({'message': 'error creating logged exercise set'}), 500)

# Update a logged exercise set
@logged_exercise_sets.route('/<int:loggedExerciseSetId>', methods=['PUT'])
def update_logged_exercise_set(loggedExerciseSetId):
    try:
        logged_exercise_set = LoggedExerciseSet.query.filter_by(loggedExerciseSetId=loggedExerciseSetId).first()
        if logged_exercise_set:
            data = request.get_json()

            logged_exercise_set.loggedRoutineId = data['loggedRoutineId']
            logged_exercise_set.loggedRoutineSetId = data['loggedRoutineSetId']
            logged_exercise_set.weight = data['weight']
            logged_exercise_set.reps = data['reps']
            logged_exercise_set.setOrder = data['setOrder']
            logged_exercise_set.isWarmupSet = data['isWarmupSet']
            logged_exercise_set.notes = data['notes']
            logged_exercise_set.userUID = data['userUID']

            db.session.commit()
            return make_response(jsonify({'message': 'logged exercise set updated'}), 200)
        return make_response(jsonify({'message': 'logged exercise set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error updating logged exercise set'}), 500)

# Delete a logged exercise set
@logged_exercise_sets.route('/<int:loggedExerciseSetId>', methods=['DELETE'])
def delete_logged_exercise_set(loggedExerciseSetId):
    try:
        logged_exercise_set = LoggedExerciseSet.query.filter_by(loggedExerciseSetId=loggedExerciseSetId).first()
        if logged_exercise_set:
            db.session.delete(logged_exercise_set)
            db.session.commit()
            return make_response(jsonify({'message': 'logged exercise set deleted'}), 200)
        return make_response(jsonify({'message': 'logged exercise set not found'}), 404)
    except:
        return make_response(jsonify({'message': 'error deleting logged exercise set'}), 500)
