from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable= False, unique = True)
    todos = db.Column(db.String, nullable= True, default = "")

    def serialize(self):
        return json.loads(self.todos)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()