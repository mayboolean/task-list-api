from flask import Blueprint, Response, request
from ..models.goal import Goal
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.obj_from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    response = {"goal": new_goal.obj_to_dict()}
    return response, 201
