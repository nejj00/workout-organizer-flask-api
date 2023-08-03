from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import Exercise, db
#import src.constants.http_status_codes

exercises = Blueprint("exercises", __name__, url_prefix="/api/exercises")

@exercises.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'exercises test'}), 200)

# create an exercise
@exercises.route('/', methods=['POST'])
def create_exercise():
  try:
    data = request.get_json()
    new_exercise = Exercise(
      categoryId=['categoryId'], 
      name=data['name'], 
      type=data['type'], 
      isSingleSide=['isSingleSide'], 
      isUserMade=data['isUserMade'], 
      userUID=data['userUID']
      )
    
    db.session.add(new_exercise)
    db.session.commit()
    return make_response(jsonify({'message': 'exercise created'}), 201)
  except:
    return make_response(jsonify({'message': 'error creating exercise'}), 500)

# get all exercises
@exercises.route('/', methods=['GET'])
def get_exercises():
  try:
    exercises = Exercise.query.all()
    return make_response(jsonify([exercise.json() for exercise in exercises]), 200)
  except:
    return make_response(jsonify({'message': 'error getting exercises'}), 500)
  
  
# delete an exercise
@exercises.route('/<int:exerciseId>', methods=['DELETE'])
def delete_exercise(exerciseId):
  try:
    exercise = Exercise.query.filter_by(exerciseId=exerciseId).first()
    if exercise:
      db.session.delete(exercise)
      db.session.commit()
      return make_response(jsonify({'message': 'exercise deleted'}), 200)
    return make_response(jsonify({'message': 'exercise not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error deleting exercise'}), 500)