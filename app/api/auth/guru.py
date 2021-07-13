from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from api.models import Guru
from api import db
import datetime

guru = Blueprint('guru', __name__)

@guru.route('/guru_register', methods=["POST"])
def guru_register():
    params = request.form
    # validate the existence of params
    if not params.get('nama_guru'):
        return make_response(jsonify({'error': 'Nama Guru diperlukan!'}), 400)
    if not params.get('nip'):
        return make_response(jsonify({'error': 'NIP diperlukan!'}), 400)
    if not params.get('isWaliKelas'):
        return make_response(jsonify({'error': 'Status wali kelas diperlukan!'}), 400)
    if not params.get('isActive'):
        return make_response(jsonify({'error': 'Status aktif diperlukan!'}), 400)
    if not params.get('username'):
        return make_response(jsonify({'error': 'Username diperlukan!'}), 400)
    if not params.get('password'):
        return make_response(jsonify({'error': 'Password diperlukan!'}), 400)
    
    # Validate isWaliKelas
    if int(params.get('isWaliKelas')) not in (0, 1):
        return make_response(jsonify({'error': 'isWaliKelas harus 0 atau 1'}), 400)
    if int(params.get('isActive')) not in (0, 1):
        return make_response(jsonify({'error': 'isAcitve harus 0 atau 1'}), 400)

    # if Username already exists, reject the attempt
    existing_username = Guru.query.filter_by(username=params.get('username')).first()
    if existing_username:
        return make_response(jsonify({'error': 'Username sudah ada!'}), 400)
    # Process the registering
    user = Guru(**params)
    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'message': 'Register success'}), 200)

@guru.route('/guru_login', methods=["POST"])
def guru_login():
    params = request.form
    # validate the existence of params
    if not params.get('username'):
        return make_response(jsonify({'error': 'Username diperlukan!'}), 400)
    if not params.get('password'):
        return make_response(jsonify({'error': 'Password diperlukan!'}), 400)
    # check the login
    user = Guru.query.filter_by(username=params.get('username')).first()
    authorized = user.check_password(params.get('password'))
    if not authorized:
        return make_response(jsonify({'error': 'Email or password invalid'}), 401)
    
    # Create access token
    expires = datetime.timedelta(days=2)
    access_token = create_access_token(identity=str(user.id_guru), expires_delta=expires)
    return make_response(jsonify({'message': 'login success', 'token': access_token}), 200)