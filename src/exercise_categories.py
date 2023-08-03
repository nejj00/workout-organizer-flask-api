from flask import Blueprint, Flask, request, jsonify, make_response
from src.database import ExerciseCategory, db
#import src.constants.http_status_codes

exercise_categories = Blueprint("exercise_categories", __name__, url_prefix="/api/exercise_categories")

@exercise_categories.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'exercise categories test'}), 200)


# create an exercise category
@exercise_categories.route('/', methods=['POST'])
def create_exercise_category():
  try:
    data = request.get_json()
    new_exercise_category = ExerciseCategory(name=data['name'], isUserMade=data['isUserMade'], userUID=data['userUID'])
    db.session.add(new_exercise_category)
    db.session.commit()
    return make_response(jsonify({'message': 'exercise category created'}), 201)
  except:
    return make_response(jsonify({'message': 'error creating exercise category'}), 500)

# get all exercise categories
@exercise_categories.route('/', methods=['GET'])
def get_exercise_categories():
  try:
    exercise_categories = ExerciseCategory.query.all()
    return make_response(jsonify([exercise_category.json() for exercise_category in exercise_categories]), 200)
  except:
    return make_response(jsonify({'message': 'error getting exercise categories'}), 500)

# update an exercise category
@exercise_categories.route('/<int:categoryId>', methods=['PUT'])
def update_exercise_category(categoryId):
  try:
    exercise_category = ExerciseCategory.query.filter_by(categoryId=categoryId).first()
    if exercise_category:
      data = request.get_json()
      
      exercise_category.name = data['name']
      exercise_category.isUserMade = data['isUserMade']
      exercise_category.userUID = data['userUID']
      
      db.session.commit()
      return make_response(jsonify({'message': 'exercise category updated'}), 200)
    return make_response(jsonify({'message': 'exercise category not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error updating exercise category'}), 500)

# delete an exercise category
@exercise_categories.route('/<int:categoryId>', methods=['DELETE'])
def delete_exercise_category(categoryId):
  try:
    exercise_category = ExerciseCategory.query.filter_by(categoryId=categoryId).first()
    if exercise_category:
      db.session.delete(exercise_category)
      db.session.commit()
      return make_response(jsonify({'message': 'exercise category deleted'}), 200)
    return make_response(jsonify({'message': 'exercise category not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error deleting exercise category'}), 500)