from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class ExerciseCategory(db.Model):
    __tablename__ = "exercise_categories"

    categoryId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, default="")
    isUserMade = db.Column(db.Boolean, nullable=False, default=False)
    userUID = db.Column(db.String)

    exercises = db.relationship("Exercise", backref="exerciseCategory")

    def json(self):
        return {
            'categoryId': self.categoryId,
            'name': self.name,
            'isUserMade': self.isUserMade,
            'userUID': self.userUID
            }
        
        
class Exercise(db.Model):
    __tablename__ = "exercises"

    exerciseId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryId = db.Column(db.Integer, db.ForeignKey(ExerciseCategory.categoryId), nullable=False)
    name = db.Column(db.String, nullable=False, default="")
    type = db.Column(db.String, nullable=False, default="")
    isSingleSide = db.Column(db.Boolean, nullable=False, default=False)
    isUserMade = db.Column(db.Boolean, nullable=False, default=False)
    userUID = db.Column(db.String)
    
    routineSets = db.relationship('RoutineSet', backref="exercise")
    loggedRoutineSets = db.relationship("LoggedRoutineSet", backref="exercise")

    def json(self):
        return {
            'exerciseId': self.exerciseId,
            'categoryId': self.categoryId,
            'name': self.name,
            'type': self.type,
            'isSingleSide': self.isSingleSide,
            'isUserMade': self.isUserMade,
            'userUID': self.userUID
        }
        
class WorkoutRoutine(db.Model):
    __tablename__ = "workout_routines"

    routineId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, default="")
    notes = db.Column(db.String, nullable=False, default="")
    isUserMade = db.Column(db.Boolean, nullable=False, default=False)
    userUID = db.Column(db.String, nullable=True)
    
    routineSets = db.relationship('RoutineSet', backref='workoutRoutine')

    def json(self):
        return {
            'routineId': self.routineId,
            'name': self.name,
            'notes': self.notes,
            'isUserMade': self.isUserMade,
            'userUID': self.userUID
        }
        
class RoutineSet(db.Model):
    __tablename__ = "routine_sets"

    routineSetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    routineId = db.Column(db.Integer, db.ForeignKey(WorkoutRoutine.routineId), nullable=False)
    exerciseId = db.Column(db.Integer, db.ForeignKey(Exercise.exerciseId), nullable=False)
    warmupSetsCount = db.Column(db.Integer, default=0)
    setsCount = db.Column(db.Integer, default=0)
    setsOrder = db.Column(db.Integer, default=0)
    isUserMade = db.Column(db.Boolean, nullable=False, default=False)
    userUID = db.Column(db.String, nullable=False, default="")
    
    def json(self):
        return {
            'routineSetId': self.routineSetId,
            'routineId': self.routineId,
            'exerciseId': self.exerciseId,
            'warmupSetsCount': self.warmupSetsCount,
            'setsCount': self.setsCount,
            'setsOrder': self.setsOrder,
            'isUserMade': self.isUserMade,
            'userUID': self.userUID
        }
        
class LoggedWorkoutRoutine(db.Model):
    __tablename__ = "logged_workout_routines"

    loggedRoutineId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, default="")
    bodyweight = db.Column(db.Float, default=0.0)
    notes = db.Column(db.String, nullable=False, default="")
    date = db.Column(db.Date, default=datetime.date.today)
    startTime = db.Column(db.Time, default=datetime.datetime.now().time)
    endTime = db.Column(db.Time)
    userUID = db.Column(db.String)

    loggedRoutineSet = db.relationship("LoggedRoutineSet", backref="loggedWorkoutRoutine")
    loggedExerciseSets = db.relationship("LoggedExerciseSet", backref="loggedWorkoutRoutine")

    def json(self):
        return {
            'loggedRoutineId': self.loggedRoutineId,
            'name': self.name,
            'bodyweight': self.bodyweight,
            'notes': self.notes,
            'date': self.date.isoformat(),
            'startTime': self.startTime.isoformat(),
            'endTime': self.endTime.isoformat() if self.endTime else None,
            'userUID': self.userUID
        }
        
class LoggedRoutineSet(db.Model):
    __tablename__ = "logged_routine_sets"

    loggedRoutineSetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loggedRoutineId = db.Column(db.Integer, db.ForeignKey(LoggedWorkoutRoutine.loggedRoutineId))
    exerciseId = db.Column(db.Integer, db.ForeignKey(Exercise.exerciseId))
    exerciseName = db.Column(db.String, nullable=False, default="")
    warmupSetsCount = db.Column(db.Integer, default=0)
    setsCount = db.Column(db.Integer, default=0)
    setsOrder = db.Column(db.Integer, default=0)
    userUID = db.Column(db.String)
    
    loggedExerciseSets = db.relationship("LoggedExerciseSet", backref="loggedRoutineSet")

    def json(self):
        return {
            'loggedRoutineSetId': self.loggedRoutineSetId,
            'loggedRoutineId': self.loggedRoutineId,
            'exerciseId': self.exerciseId,
            'exerciseName': self.exerciseName,
            'warmupSetsCount': self.warmupSetsCount,
            'setsCount': self.setsCount,
            'setsOrder': self.setsOrder,
            'userUID': self.userUID
        }
        
class LoggedExerciseSet(db.Model):
    __tablename__ = "logged_exercise_sets"

    loggedExerciseSetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loggedRoutineId = db.Column(db.Integer, db.ForeignKey(LoggedWorkoutRoutine.loggedRoutineId))
    loggedRoutineSetId = db.Column(db.Integer, db.ForeignKey(LoggedRoutineSet.loggedRoutineSetId))
    weight = db.Column(db.Float, default=0.0)
    reps = db.Column(db.Integer, default=0)
    setOrder = db.Column(db.Integer, default=0)
    isWarmupSet = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String, nullable=False, default="")
    userUID = db.Column(db.String)

    def json(self):
        return {
            'loggedExerciseSetId': self.loggedExerciseSetId,
            'loggedRoutineId': self.loggedRoutineId,
            'loggedRoutineSetId': self.loggedRoutineSetId,
            'weight': self.weight,
            'reps': self.reps,
            'setOrder': self.setOrder,
            'isWarmupSet': self.isWarmupSet,
            'notes': self.notes,
            'userUID': self.userUID
        }
        
class User(db.Model):
    __tablename__ = "users"

    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userUID = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    bodyweight = db.Column(db.Float, default=0.0)
    userCreated = db.Column(db.DateTime)
    userLastLogin = db.Column(db.DateTime)

    def json(self):
        return {
            'userId': self.userId,
            'userUID': self.userUID,
            'email': self.email,
            'bodyweight': self.bodyweight,
            'userCreated': self.userCreated.isoformat(),
            'userLastLogin': self.userLastLogin.isoformat()
        }