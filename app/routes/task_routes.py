from flask import Blueprint, request, Response, abort, make_response
from ..models.task import Task
from ..db import db


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# make a POST request to /tasks with the following HTTP request body
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    title = request_body.get("title", None)
    description = request_body.get("description", None)
    completed_at = request_body.get("completed_at", None)

    if not title or not description:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()
 
    response = {"task": dict(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        is_complete=True if new_task.completed_at is not None else False
    )}

    return response, 201

# GET request to /tasks
@tasks_bp.get("")
def get_all_task():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(dict(
            id=task.id,
            title=task.title,
            description=task.description,
            is_complete=True if task.completed_at is not None else False
        ))
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task": dict(
        id=task.id,
        title=task.title,
        description=task.description,
        is_complete=True if task.completed_at is not None else False
    )}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return { "task": dict(
        id=task.id,
        title=task.title,
        description=task.description,
        is_complete=True if task.completed_at is not None else False
    )}

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"Task {task_id} is invalid"}
        abort(make_response(response, 400))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"Task {task_id} was not found"}
        abort(make_response(response, 404))

    return task    

