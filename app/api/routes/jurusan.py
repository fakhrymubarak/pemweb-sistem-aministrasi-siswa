from flask import Blueprint, request, jsonify, make_response
from api.schema.jurusan import JurusanSchema
from api.models import Jurusan
from api import db

jurusan = Blueprint('jurusan', __name__)

@jurusan.route('/jurusan', methods=['GET', 'POST'])
def get_post_jurusan():
    # GET ALL JURUSAN
    if request.method == "GET":
        all_jurusan = db.session.query(Jurusan).all()
        schema = JurusanSchema(many=True)
        result = schema.dump(all_jurusan)
        return make_response(jsonify({"jurusan": result}), 200)
    # POST JURUSAN
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('nama_jurusan'):
            return make_response(jsonify({'error': 'Nama jurusan diperlukan!'}), 400)
        # Query to the model
        schema = JurusanSchema()
        jurusan = schema.load(params)
        db.session.add(jurusan)
        db.session.commit()
        # make JSON response
        result = schema.dump(jurusan)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)

@jurusan.route('/jurusan/<id_jurusan>', methods=["GET", "DELETE"])
def jurusan_by_id(id_jurusan):
    # GET ONE JURUSAN
    if request.method == "GET":
        get_jurusan = db.session.query(Jurusan).get(id_jurusan)
        schema = JurusanSchema()
        result = schema.dump(get_jurusan)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # DELETE ONE JURUSAN
    if request.method == "DELETE":
        get_jurusan = db.session.query(Jurusan).get(id_jurusan)
        db.session.delete(get_jurusan)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)