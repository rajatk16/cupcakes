"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template

from models import connect_db, db, Cupcake

app = Flask(__name__)
app.config["SECRET_KEY"] = "goldtree9"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
# db.drop_all()
# db.create_all()

# Route Routes
@app.route("/")
def root():
  return render_template('index.html')

# List all Cupcakes as JSON
@app.route("/api/cupcakes")
def all_cupcakes():
  cupcakes = [cupcake.to_dict for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes=cupcakes)

# Get a Cupcake as JSON
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id).to_dict
  return jsonify(cupcake=cupcake)

# Create a new Cupcake
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
  data = request.json

  cupcake = Cupcake(
    flavor = data["flavor"],
    rating = data["rating"],
    size = data["size"],
    image = data["image"] or None
  )

  db.session.add(cupcake)
  db.session.commit()

  return (jsonify(cupcake=cupcake.to_dict), 201)

# Update a cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
  data = request.json

  cupcake = Cupcake.query.get_or_404(cupcake_id)

  cupcake.flavor = data["flavor"]
  cupcake.size = data["size"]
  cupcake.rating = data["rating"]
  cupcake.image = data["image"]

  db.session.add(cupcake)
  db.session.commit()

  return jsonify(cupcake=cupcake.to_dict)

# Delete a cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  db.session.delete(cupcake)
  db.session.commit()

  return jsonify(message="Deleted")