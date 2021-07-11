from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from api.models import Admin
from api import db
import datetime

super_admin = Blueprint('super_admin', __name__)

@super_admin.route('/admin_register', methods=["POST"])
def super_admin_register():
    params = request.form
    # validate the existence of params
    if not params.get('username'):
        return make_response(jsonify({'error': 'Username diperlukan!'}), 400)
    if not params.get('password'):
        return make_response(jsonify({'error': 'Password diperlukan!'}), 400)
    # Process the registering
    user = Admin(**params)
    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'message': 'OK'}), 200)

@super_admin.route('/admin_login', methods=["POST"])
def super_admin_login():
    params = request.form
    user = db.session.query(Admin).filter_by(username=params.get('username')).first()
    # validate the existence of params
    if not params.get('username'):
        return make_response(jsonify({'error': 'Username diperlukan!'}), 400)
    if not params.get('password'):
        return make_response(jsonify({'error': 'Password diperlukan!'}), 400)
    authorized = user.check_pasword(params.get('password'))
    if not authorized:
        return make_response(jsonify({'error': 'Email or password invalid'}), 401)
    
    # Create access token
    expires = datetime.timedelta(days=2)
    access_token = create_access_token(identity=str(user.id_admin), expires_delta=expires)
    return make_response(jsonify({'token': access_token}), 200)
    