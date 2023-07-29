from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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