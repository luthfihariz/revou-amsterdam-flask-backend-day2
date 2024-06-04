from flask import Blueprint, request, jsonify
from flasgger import swag_from

user_blueprint = Blueprint("user", __name__)

users = []


@user_blueprint.route("/register", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "User",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "The username for the new user",
                        },
                        "password": {
                            "type": "string",
                            "description": "The password for the new user",
                        },
                    },
                },
            }
        ],
        "responses": {
            201: {
                "description": "User registered!",
                "schema": {
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "A message confirming the user registration",
                        },
                        "user": {
                            "type": "object",
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "The username of the registered user",
                                },
                            },
                        },
                    },
                },
            },
            400: {
                "description": "Username or password is not provided",
                "schema": {
                    "properties": {
                        "error": {
                            "type": "string",
                            "description": "An error message indicating that the username or password is not provided",
                        },
                    },
                },
            },
        },
    }
)
def register():
    """
    Register a new user
    ---
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username and password:
        users.append({"username": username, "password": password})
        return (
            jsonify({"message": "User registered!", "user": {"username": username}}),
            201,
        )
    else:
        return jsonify({"error": "Username or password is not provided"}), 400


@user_blueprint.route("/login", methods=["POST"])
@swag_from("docs/login.yml")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = None
    for u in users:
        if u["username"] == username and u["password"] == password:
            user = u
            break

    if user:
        return jsonify({"message": "Logged in!", "user": {"username": username}}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 400
