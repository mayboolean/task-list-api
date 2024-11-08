from flask import Blueprint, request, Response, abort, make_response
from ..models.task import Task
from ..db import db
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# make a POST request to /tasks with the following HTTP request body
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = Task.obj_from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
 
    response = {"task": new_task.obj_to_dict()}

    return response, 201

# GET request to /tasks
@tasks_bp.get("")
def get_all_task():
    query = db.select(Task)
    sort =  request.args.get("sort")

    if sort == "asc":
        query = query.order_by(Task.title.asc())
    elif sort == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = [task.obj_to_dict() for task in tasks]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task": task.obj_to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return { "task": task.obj_to_dict()}

@tasks_bp.patch("/<task_id>/<mark_as>")
def update_is_complete(task_id, mark_as):
    task = validate_task(task_id)

    if mark_as == "mark_complete":
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    
    db.session.commit()

    return { "task": task.obj_to_dict()}

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

