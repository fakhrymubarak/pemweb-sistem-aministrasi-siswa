from flask import Blueprint, request, jsonify, make_response
from api.schema.kelas import KelasSchema
from api.models import Kelas
from api import db
from flask_jwt_extended import jwt_required

kelas = Blueprint('kelas', __name__)

@kelas.route('/kelas', methods=["GET", "POST"])
@jwt_required()
def get_post_kelas():
    # GET ALL KELAS
    if request.method == "GET":
        all_kelas = db.session.query(Kelas).all()
        schema = KelasSchema(many=True)
        result = schema.dump(all_kelas)
        return make_response(jsonify({"kelas": result}), 200)
    # POST KELAS
    elif request.method == "POST":
        params = request.form
        # Validate the form (case: params not exist)
        if not params.get('jenjang_kelas'):
            return make_response(jsonify({'error': 'Jenjang kelas diperlukan!'}), 400)
        if not params.get('urutan_kelas'):
            return make_response(jsonify({'error': 'Urutan kelas diperlukan!'}), 400)
        if not params.get('id_jurusan'):
            return make_response(jsonify({'error': 'Id Jurusan diperlukan!'}), 400)
        if not params.get('wali_kelas'):
            return make_response(jsonify({'error': 'ID Wali kelas diperlukan!'}), 400)

        # Validate the form (case: params not valid)
        if params.get('jenjang_kelas') not in ('X', 'XI', 'XII'):
            return make_response(jsonify({'error': 'Jenjang kelas tidak valid!'}), 400)
        if params.get('urutan_kelas') not in ('A', 'B', 'C', 'D'):
            return make_response(jsonify({'error': 'Urutan kelas tidak valid!'}), 400)

        # Query to the model
        schema = KelasSchema()
        kelas = schema.load(params)
        db.session.add(kelas)
        db.session.commit()

        # make JSON response
        result = schema.dump(kelas)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)

@kelas.route('/kelas/<id_kelas>', methods=["GET", "DELETE", "PUT"])
@jwt_required()
def kelas_by_id(id_kelas):
    # GET ONE KELAS
    if request.method == "GET":
        get_kelas = db.session.query(Kelas).get(id_kelas)
        schema = KelasSchema()
        result = schema.dump(get_kelas)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)

    # UPDATE ONE KELAS
    elif request.method == "PUT":
        params = request.form
        # if kelas doesn't exist, reject request
        get_kelas = db.session.query(Kelas).get(id_kelas)
        if get_kelas is None:
            return make_response(jsonify({'error': 'Kelas not found!'}), 404)
        # Validate jenjang_kelas and urutan_kelas
        if params.get('jenjang_kelas') and params.get('jenjang_kelas') not in ('X', 'XI', 'XII'):
            return make_response(jsonify({'error': 'Jenjang kelas tidak valid!'}), 400)
        if params.get('urutan_kelas') and params.get('urutan_kelas') not in ('A', 'B', 'C', 'D'):
            return make_response(jsonify({'error': 'Urutan kelas tidak valid!'}), 400)

        # Update kelas based on params
        for p in params:
            setattr(get_kelas, p, request.form[p])
        db.session.commit()
        # Create JSON response
        schema = KelasSchema()
        result = schema.dump(get_kelas)
        return make_response(jsonify({'message': 'update successful', 'result': result}), 200)
        
    # DELETE ONE KELAS
    if request.method == "DELETE":
        get_kelas = db.session.query(Kelas).get(id_kelas)
        db.session.delete(get_kelas)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)