from flask import Blueprint,jsonify,request,send_from_directory
from app.models import Student
from app.db import db
import re
import os


#create student bluprint
student_bp=Blueprint("student",__name__)

UPLOAD_FOLDER="uploads"

#dymaic route
@student_bp.route("/single/<int:student_id>",methods=["GET"])
def single_student(student_id):
    
    #   student=Student.query.filter_by(id=student_id).first()
    student=Student.query.get(student_id)
    
    if not student:
        return jsonify({"message":f"Studennt with id {student_id} does not exits"})
    
    return jsonify({
         "id":student.id,
         "name":student.name,
         "email":student.email,
         "created_at":student.created_at
    })

#delete students: CREATE,READ,UPDATE , <DELETE STUDENT>
@student_bp.route("/edit/<int:student_id>",methods=["PUT"])
def edit_student(student_id):

    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({"message":f"Studennt with id {student_id} does not exits"})
    

    data=request.get_json()

    if "name" in data:
        
        student.name=data["name"]
    
    db.session.commit()

    return jsonify({
         "id":student.id,
         "name":student.name,
         "email":student.email,
         "created_at":student.created_at
    })




#adding a student to our db
#routes and controller logic
#CREATING READING UPDATING DELETE
@student_bp.route("/add/json",methods=["POST"])
def add_student_json():
    print("Add user was hit")
    data=request.get_json() 

    name=data.get("name")
    email=data.get("email")

    if not name:
        return jsonify({"error":"Name is required"}),400
    
    if not email:
        return jsonify({"error":"Email is required"}),400

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_regex,email):
        return jsonify({"error":"Invalid email address"})
    
    #Existing student
    exists=Student.query.filter_by(email=email).first()

    if exists:
        return jsonify({"error":"Email in use"}),400
    
    new_student=Student(name=name,email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message":"Student added",
        "student":{
            "id":new_student.id,
            "name":new_student.name,
            "email":new_student.email,
            "created_at":new_student.created_at
        }
    }),201


@student_bp.route("/add/form",methods=["POST"])
def add_student_form():
    # print("Add user was hit")
    # data=request.get_json() 

    name=request.form.get("name")
    email=request.form.get("email")

    if not name:
        return jsonify({"error":"Name is required"}),400
    
    if not email:
        return jsonify({"error":"Email is required"}),400

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_regex,email):
        return jsonify({"error":"Invalid email address"})
    
    #Existing student
    exists=Student.query.filter_by(email=email).first()

    if exists:
        return jsonify({"error":"Email in use"}),400
    
    new_student=Student(name=name,email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message":"Student added",
        "student":{
            "id":new_student.id,
            "name":new_student.name,
            "email":new_student.email,
            "created_at":new_student.created_at
        }
    }),201

@student_bp.route("/picture",methods=["POST"])
def add_student_picture():
   
    ALLOWED_EXTENSIONS={"png","jpg","jpeg"}

    #make sure folder exists
    os.makedirs(UPLOAD_FOLDER,exist_ok=True)

    if "pic" not in request.files:
        return jsonify({"error":"No file"}),400
    
    file=request.files["pic"]

    if file.filename=="":
        return jsonify({"error":"No file selected"}),400
    
    filename=file.filename

    ext=filename.rsplit(".",1)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error":"Invalid file type"}),400
    
    filepath=os.path.join(UPLOAD_FOLDER,filename)
    file.save(filepath)

    return jsonify({
        "message":"File uploaded succefully",
        "filename":filename,
        "path":filepath
    }),201

#dynamic route :REACT<>
#---file serving --
@student_bp.route("/picture/<filename>",methods=["GET"])
def serve_file(filename):

    # print("Dynamic route is")
    # print(filename)
    # return "dynamic route"
    # print("file hit")
    # #puts the filename as part of the request
    cwd=os.path.dirname(__file__)
    uploads=os.path.join(cwd,"../../uploads")
    return send_from_directory(uploads,filename)



@student_bp.route("/list",methods=["GET"])
def list_users():
    students=Student.query.all()

    print(students)
    student_list=[]

    for student in students:
        student_list.append({
            "id":student.id,
            "name":student.name,
            "email":student.email,
            "created_at":student.created_at
        })

    print(student_list)

    return jsonify({
        "students":student_list,
        "count":len(student_list)
    }),200

#geting a single student
#Updating student -> 
# Reading then 