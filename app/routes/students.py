from flask import Blueprint,jsonify,request

#student blueprint

student_bp=Blueprint("student",__name__)

#routes and controller logic 

@student_bp.route("/students/add",methods=["POST"] ) 
def add_user():
    print("Add user was hit")
    return "Added a user"


@student_bp.route("/students",methods=["GET"] ) 
def list_user():
    print("List students")
    return "List All students"