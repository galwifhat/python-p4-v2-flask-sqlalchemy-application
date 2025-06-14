# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# avoid building up too much unhelpful data in memory when our application is running.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# migrate instance configures the application and models for Flask-Migrate
migrate = Migrate(app, db)

# connects our database to our application before it runs.
db.init_app(app)


# add views here
# determines which resources are available at which URLs
# and saves them to the application's URL map.
@app.route("/")
def index():
    response = make_response("<h1>Welcome to the pet directory!</h1>", 200)
    return response


@app.route("/pets/<int:id>")
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        response_body = f"<p>{pet.name} {pet.species}</p>"
        response_status = 200
    else:
        response_body = f"<p>Pet {id} not found</p>"
        response_status = 404
    response = make_response(response_body, response_status)
    return response


@app.route("/species/<string:species>")
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species).all()

    # The expression species=species passed into the filter_by function may be a bit confusing.
    # The species before the equal sign refers to the table column,
    # while species after the equal sign refers to the route parameter.

    size = len(pets)  # all() returns a list so we can get length
    response_body = f"<h2>There are {size} {species}s</h2>"
    for pet in pets:
        response_body += f"<p>{pet.name}</p>"
    response = make_response(response_body, 200)
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
