from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

api = Flask(__name__)

api.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(api)
CORS(api)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

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