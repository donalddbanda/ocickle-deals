from flask import current_app
from .extensions import db
from app.models import WaitingList, Admin
from flask import request, jsonify, Blueprint
from flask_login import current_user, login_user, login_required

waiting_list_bp = Blueprint("waiting-list", __name__, url_prefix="/waiting-list")
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@waiting_list_bp.route('/join', methods=["POST"])
def join_waiting_list():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    if not name:
        return jsonify({"message": "Name not provided", "success": False}), 400

    if not email or not phone:
        return jsonify({"message": "Email or phone number not provided", "success": False}), 400
    
    if email and WaitingList.query.filter_by(email=email).first():
        return jsonify({"message": "you already subscribed"}), 200
    
    if phone and WaitingList.query.filter_by(phone=phone).first():
        return jsonify({"message": "you already subscribed"}), 200

    waiting_list_user = WaitingList(name=name, email=email, phone=phone)
    
    try:
        db.session.add(waiting_list_user)
        db.session.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"message": "An error occured", "error": str(e), "success": False}), 500


@waiting_list_bp.route("/get")
@login_required
def get_waiting_list_members():

    if current_user.is_anonymous:
        return jsonify({"message": "login required", "success": False}), 401
    
    if current_user.role.lower() == "admin":
        return jsonify({"message": "access denied", "success": False}), 403

    waiting_list_members = WaitingList.query.paginate()

    return jsonify({
        "members": waiting_list_members.items, 
        "total": waiting_list_members.total, 
        "has_next": waiting_list_members.has_next(), 
        "has_prev": waiting_list_members.has_prev() 
    })


@admin_bp.route("/login", methods=["POST"])
@login_required
def admin_login():
    data = request.get_json()

    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not email or not phone:
        return jsonify({"message": "Email or phone number not provided", "success": False}), 400
    
    if not password:
        return jsonify({"message": "Password is required", "success": False}), 400
    
    if email:
        admin = Admin.query.filter_by(email=email).first()
    else:
        admin = Admin.query.filter_by(phone=phone).first()

    if not admin:
        return jsonify({"message": "admin not found", "success": False}), 400

    if not admin.verify_password(password):
        return jsonify({"message": "incorrect password", "success": False}), 400
    
    try:
        login_user(admin)
        return jsonify({
            "success": True,
            "message": "login successful"
        })
    except Exception as e:
        return jsonify({
            "message": "An error occured",
            "success": False,
            "error": str(e)
        }), 500


@admin_bp.route("/register", methods=["POST"])
def admin_register():

    if Admin.query.filter_by(role="admin").first():
        return jsonify({"message": "an error occured", "success": False}), 400

    data = request.get_json()

    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    

    if not email or not phone:
        return jsonify({"error": "Email or phone number not provided"}), 400
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    if Admin.query.filter_by(email=email).first():
        return jsonify({"message": "email already used"}), 200
    
    if Admin.query.filter_by(phone=phone).first():
        return jsonify({"message": "phone already used"}), 200

    admin = Admin(email=email, phone=phone)
    admin.set_password(password)

    try:
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "registration successful", "success": True}), 201

    except Exception as e:
        return jsonify({"error": str(e), "message": "an error occured", "success": False}), 400