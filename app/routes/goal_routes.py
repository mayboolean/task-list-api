from flask import Blueprint, Response, request, abort, make_response
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

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [goal.obj_to_dict() for goal in goals]
    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {"goal": goal.obj_to_dict()}, 200


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"Goal {goal_id} is invalid"}
        abort(make_response(response, 400))
    
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"Goal {goal_id} was not found"}
        abort(make_response(response, 404))

    return goal