from flask import Blueprint, request, jsonify, make_response
from api.schema.siswa import SiswaSchema
from api.models import Siswa, Kelas
from api import db
from flask_jwt_extended import jwt_required

siswa = Blueprint('siswa', __name__)

@siswa.route('/siswa', methods=["GET", "POST"])
@jwt_required()
def get_post_siswa():
    # GET ALL SISWA
    if request.method == "GET":
        all_siswa = db.session.query(Siswa).join(Kelas).all()
        schema = SiswaSchema(many=True)
        result = schema.dump(all_siswa)
        return make_response(jsonify({"siswa": result}), 200)
    # POST SISWA
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('nis'):
            return make_response(jsonify({'error': 'NIS diperlukan!'}), 400)
        if not params.get('nama_siswa'):
            return make_response(jsonify({'error': 'Nama diperlukan!'}), 400)
        if not params.get('email'):
            return make_response(jsonify({'error': 'Email diperlukan!'}), 400)
        if not params.get('jenkel'):
            return make_response(jsonify({'error': 'Jenkel diperlukan!'}), 400)
        if not params.get('id_kelas'):
            return make_response(jsonify({'error': 'id_kelas diperlukan!'}), 400)
        if params.get('jenkel') not in ('L', 'P'):
            return make_response(jsonify({'error': 'jenis kelamin tidak valid!'}), 400)
        # If siswa already exist, reject request
        if db.session.query(Siswa).get(params['nis']):
            return make_response(jsonify({'error': 'Siswa with this NIS already exist!'}), 400)
        # Query to the model
        schema = SiswaSchema()
        siswa = schema.load(params)
        db.session.add(siswa)
        db.session.commit()
        # make JSON response
        result = schema.dump(siswa)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)

@siswa.route('/siswa/<nis>', methods=["GET", "DELETE", "PUT"])
@jwt_required()
def siswa_by_nis(nis):
    # GET ONE SISWA
    if request.method == "GET":
        get_siswa = db.session.query(Siswa).get(nis)
        schema = SiswaSchema()
        result = schema.dump(get_siswa)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # UPDATE ONE SISWA
    elif request.method == "PUT":
        params = request.form
        # if siswa doesn't exist, reject request
        get_siswa = db.session.query(Siswa).get(nis)
        if get_siswa is None:
            return make_response(jsonify({'error': 'Siswa not found!'}), 404)
        # Validate jenis_kelamin
        if params.get('jenkel') and params.get('jenkel') not in ('L', 'P'):
            return make_response(jsonify({'error': 'Jenis kelamin tidak valid!'}), 400)
        # Update siswa based on params
        for p in params:
            setattr(get_siswa, p, request.form[p])
        db.session.commit()
        # Create JSON response
        schema = SiswaSchema()
        result = schema.dump(get_siswa)
        return make_response(jsonify({'message': 'update successful', 'result': result}), 200)
    # DELETE ONE SISWA
    if request.method == "DELETE":
        get_siswa = db.session.query(Siswa).get(nis)
        db.session.delete(get_siswa)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)