

from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

##################################################     
#           VALIDATE MODEL ID  
##################################################

def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        class_name=cls.__name__.lower()
        abort(make_response({"message":f"{class_name} {model_id} not found"}, 404))

    return model
    
################################################ 
#       WAVE 1, part 3: VALIDATE INPUT REQUESTS  
# ##############################################
def validate_task(request_body):
    try:
        if request_body['title'] and request_body['description']:
            return request_body
    except KeyError as error:
        abort(make_response({"details":"Invalid data"}, 400))

######################  WAVE 1, PART 1: CRUD ######################

#########################################
#            CREATE RESOURCE
##########################################
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    #the next line would create dependency with validate_task function
    new_task = validate_task(request_body)
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    task={"task":new_task.to_dict()}

    return task, 201

################################
#       GET ALL RESOURCES
################################
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    if request.args.get("sort")=='asc':
        tasks = Task.query.order_by(Task.title).all()
    elif request.args.get("sort")=='desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = []  #returns empty list if no tasks

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response), 200

########################################
#       Get One Task: One Saved Task
########################################
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model_id(Task, id)
    saved_task={"task":task.to_dict()}

    return saved_task,200


##################################
#       Update Task  
# ################################
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model_id(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    updated_task={"task":task.to_dict()}

    return updated_task,200


#######################################   
#           Delete Task
#######################################
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model_id(Task, id)
    title=str(task.title)
    description=str(task.description)
    #message='Task '+str(id)+" "+title+" "+description+" successfully deleted"
    message=f'Task {id} {title} successfully deleted'
    deleted_task={}
    deleted_task["details"]=message

    db.session.delete(task)
    db.session.commit()


    return deleted_task, 200

######################################   
#   FLASK SHUTDOWN ROUTE 
# #####################################
@tasks_bp.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."

############################################
#               WAVE 4
#############################################
# from flask import render_template
# import urllib.request, json
import os
from pathlib import Path
import requests

def post_message_to_slack(task_title):
    
    path = "https://slack.com/api/chat.postMessage"

    slack_token = os.environ.get("SLACK_TOKEN")
    slack_channel = 'task-notifications' 
    text = f"Someone just completed the task {task_title}"

    query_params = {
        "token": slack_token,
        "channel": slack_channel,
        "text": text
    }
    
    r = requests.post(path, query_params)

    # REFACTOR?
    # Consider using the keyword argument data, json, and/or headers



####################################################

#                WAVE 3  - PATCH

#####################################################

#############   COMPLETE_TASK: PATCH    ################
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def completed_task(id):
    task = validate_model_id(Task, id)

    #request_body = request.get_json()
    
    #if not task.completed_at:
    task.completed_at = datetime.utcnow()

    db.session.commit()

    completed_task={"task":task.to_dict()}
    completed_task["task"]["is_complete"] = True

    #add rest of message after this works
    #set text=completed_task["task"]['title']

    #alt call to post_message_to_slack("You passed Wave 4", blocks = None)
    post_message_to_slack(completed_task["task"]['title'])

    return completed_task,200

    ##sample code from FLASK docs
    

    # slack token saved in .env SLACK_TOKEN


#######################################################
#           INCOMPLETE TASK - PATCH
#######################################################
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_model_id(Task, id)

    # request_body = request.get_json()
    
    # if task.completed_at:
    task.completed_at = None

    db.session.commit()

    incomplete_task={"task":task.to_dict()}
    incomplete_task["task"]["is_complete"] = False

    return incomplete_task,200



    """##################################
#       General error handling
###################################
#@app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html', pic=pic), 404

# @app.errorhandler(400)
# def bad_request():
#     #Bad request.#
#     return make_response(
#         render_template("400.html"),
#         400
#     )


# @app.errorhandler(500)
# def server_error():
#     #Internal server error.#
#     return make_response(
#         render_template("500.html"),
#         500
#     )
    """

#################################################################
#                        WAVE 5

##########          GOALS ROUTES                    #############

##################################################################
def validate_goal(request_body):
    try:
        if request_body['title']:
            return request_body
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))

######################################
#       CREATE GOAL
########################################
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    #the next line would create dependency with validate_task function
    new_goal = validate_goal(request_body)
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    goal={"goal":new_goal.to_dict()}

    return goal, 201

#######################################
#       GET GOALS
#######################################
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    
    goals = Goal.query.all()

    goals_response = []  #returns empty list if no goals

    for goal in goals:
        goals_response.append({
                "goal_id": goal.goal_id,
                "title": goal.title,
            })

    return jsonify(goals_response), 200

#######################################
#       GET ONE GOAL
#######################################

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    saved_goal={"goal":goal.to_dict()}

    return saved_goal

##################################
#       Update Goal 
# ################################
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model_id(Goal,goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    updated_goal={"goal":goal.to_dict()}

    return updated_goal,200    

##################################
#       DELETE Goal 
# ################################

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_id(Goal,goal_id)
    db.session.delete(goal)
    db.session.commit()
    deleted_goal = {"details":f'Goal {goal_id} \"{str(goal.title)}\" successfully deleted'} 
    return deleted_goal, 200

#####################################
#         WAVE 6
######################################
def add_task_to_goal(goal_id, task_id):
    pass

######################################
#               POST
#       /GOALS/GOAL_ID/TASKS  
#####################################
@goals_bp.route("/<goal_id>/tasks",methods =["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    request_body = request.get_json()

    new_tasks=[]
    task_ids = request_body["task_ids"]
    for task_id in task_ids:
        task = validate_model_id(Task, task_id)
        new_tasks.append(task)

    goal.tasks.extend(new_tasks)

    posted_tasks={"id":int(goal_id),"task_ids":task_ids} #formatting only

    db.session.commit()#is there an update call?

    return posted_tasks
    
########################################  
#               GET 
#        /GOALS/GOAL_ID/TASKS  
########################################
@goals_bp.route("/<goal_id>/tasks",methods =["GET"])
def get_tasks_from_goal(goal_id):
    # #goal = validate_model_id(Goal, goal_id) #take goal_id, return valid goal
    # saved_goal={"goal":goal.to_dict} #get full dict for goal

    # g_tasks=[] #list of tasks to return, will return empty list if no tasks

    # # GET LIST OF TASKS FOR GOAL

    # #add .tasks to to_dict in goal model?
    # g_tasks = saved_goal.tasks #AttributeError: 'dict' object has no attribute 'tasks'
    # g_tasks = goal.tasks #TypeError: Object of type Task is not JSON serializable
    # #g_tasks = goal["tasks"] #TypeError: 'Goal' object is not subscriptable

    # return {"tasks":g_tasks} #return in required format
    #goal=Goal.query.get_or_404(goal_id)
    goal=validate_model_id(Goal,goal_id)
    return goal.to_dict(tasks=True)