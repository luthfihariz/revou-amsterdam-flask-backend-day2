from flask import Blueprint, request, jsonify

tasks_blueprint = Blueprint("tasks", __name__)

tasks = []


@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Get task list
    ---
    responses:
        200:
            description: A list of tasks
    """
    return jsonify({"tasks": tasks}), 200


@tasks_blueprint.route("/tasks", methods=["POST"])
def add_task():
    """
    Create a new task
    ---
    parameters:
      - name: task
        in: body
        schema:
            id: Task
            required:
                - task
            properties:
                task:
                    type: string
                    description: The task to be added
    responses:
      200:
        description: Task created
    """
    data = request.get_json()
    task = data.get("task")
    if task:
        tasks.append(task)
        return jsonify({"message": "Task added!", "task": task}), 201
    else:
        return jsonify({"error": "Task is not provided"}), 400


@tasks_blueprint.route("/tasks/<int:task_index>", methods=["GET"])
def get_task(task_index):
    """
    Get individual task
    ---
    parameters:
      - name: task_index
        in: path
        required: true
    responses:
      200:
        description: A single task
    """
    try:
        task = tasks[task_index]
        return jsonify({"task": task}), 200
    except IndexError:
        return jsonify({"error": "Task not found"}), 400
