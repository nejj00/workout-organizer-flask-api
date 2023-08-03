from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class ExerciseCategory(db.Model):
    __tablename__ = "exercise_categories"

    categoryId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="")
    isUserMade = db.Column(db.Boolean, nullable=False, default=False)
    userUID = db.Column(db.String)

    def json(self):
        return {
            'categoryId': self.categoryId,
            'name': self.name,
            'isUserMade': self.isUserMade,
            'userUID': self.userUID
            }
        
app.app_context().push()
db.create_all()


#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# create an exercise category
@app.route('/exercise_categories', methods=['POST'])
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
@app.route('/exercise_categories', methods=['GET'])
def get_exercise_categories():
  try:
    exercise_categories = ExerciseCategory.query.all()
    return make_response(jsonify([exercise_category.json() for exercise_category in exercise_categories]), 200)
  except:
    return make_response(jsonify({'message': 'error getting exercise categories'}), 500)

# update an exercise category
@app.route('/exercise_categories/<int:categoryId>', methods=['PUT'])
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
@app.route('/exercise_categories/<int:categoryId>', methods=['DELETE'])
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