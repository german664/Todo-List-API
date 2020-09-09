from flask import Flask, request, render_template, jsonify  
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Todo
import json


app = Flask(__name__)  
app.url_map.strict_slashes = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)  
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)


@app.route("/apis") 
def main():
    return render_template('index.html')

@app.route("/apis/todos/users", methods=['GET'])
def test_get_users():
    users = Todo.query.all()
    users_names = list(map(lambda users: users.username, users))
    if len(users_names) > 0:
        return jsonify(users_names)
    else:
        return jsonify({"msg": "No hay usuarios"})





@app.route("/apis/todos/user/<username>", methods=['GET'])  
def test_get(username=None):
    user = Todo.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Este usuario no existe"}), 404
    else:
        return jsonify(user.serialize()), 200

@app.route("/apis/todos/user/<username>", methods=['POST'])  
def test_post(username):
    user = Todo.query.filter_by(username=username).first()
    todos = request.get_json()
    if user:
        return jsonify({"msg": "Este usuario ya existe"})
    if type(todos) != list:
        return jsonify({"msg": "Debe ingresar un array vacío"})
    if len(todos) > 0:
        return jsonify({"msg": "Debe ingresar un array vacío"})

    user = Todo()
    user.username = username
    todos.append({"label": "Example", "done": "false"})
    user.todos = json.dumps(todos)
    user.save()
    return jsonify({"msg": "Usuario creado"}), 200

@app.route("/apis/todos/user/<username>", methods=['DELETE'])  
def test_delete(username):
    user = Todo.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Este usuario no existe"}), 404
    else:
        user.delete()
        return jsonify({"msg": "Usuario borrado"})

@app.route("/apis/todos/user/<username>", methods=['PUT'])  
def test_put(username):
    user = Todo.query.filter_by(username=username).first()
    todos = request.get_json()
    if not user:
        return jsonify({"msg": "Este usuario no existe"}), 404
    else:
          if type(todos) != list:
            return jsonify({"msg": "Debe ingresar un array"})
          if len(todos) == 0:
            return jsonify({"msg": "Debe ingresar un array con objetos"})
          for todo in todos:
              if len(todo) == 0:
                  return jsonify({"msg": "Debe ingresar un objeto con lleno"})
          else:
            user.todos = json.dumps(todos)
            user.update()
            return jsonify({"msg": "Se ingresaron {} tareas".format(len(todos))})
        
        
if __name__ == "__main__":  # preguntamos si esta es nuestra app principal
    manager.run()
