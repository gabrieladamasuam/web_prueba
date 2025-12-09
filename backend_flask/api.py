from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

api = Flask(__name__)

# Obtener la DATABASE_URL definida en Render
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL no está definida en Render.")

# Render puede dar la URL como postgres:// pero SQLAlchemy necesita postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

api.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(api)
CORS(api)

# Modelo Item para la prueba
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# Crear tablas automáticamente
with api.app_context():
    db.create_all()

@api.route("/ping")
def ping():
    return {"msg": "pong!"}

@api.route("/items", methods=["GET"])
def list_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "text": i.text} for i in items])

@api.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return {"msg": "Texto requerido"}, 400

    item = Item(text=text)
    db.session.add(item)
    db.session.commit()

    return {"id": item.id, "text": item.text}, 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    api.run(host="0.0.0.0", port=port)