from flask import Blueprint, request, jsonify, make_response
from api.schema.nilai import RaporNilaiSchema
from api.models import RaporNilai
from api import db

nilai = Blueprint('nilai', __name__)

@nilai.route('/nilai', methods=['GET'])
def get_nilai_individual():
    args = request.args
    form_nis = args['nis']
    form_periode = args['periode_nilai']
    query_nilai = db.session.query(RaporNilai).filter_by(nis=form_nis, periode_nilai=form_periode).all()
    schema = RaporNilaiSchema(many=True)
    result = schema.dump(query_nilai)

    # COUNT TOTAL AND AVERAGE OF NILAI
    total = avg = 0
    for item in result:
        total += item['nilai']
    avg = total / len(result)
    return make_response(jsonify({'result': result, 'total': total, 'rerata': avg}), 200)

@nilai.route('/nilai', methods=['POST'])
def post_nilai_individual():
    params = request.form
     # Validate the form
    if not params.get('nis'):
        return make_response(jsonify({'error': 'NIS diperlukan!'}), 400)
    if not params.get('periode_nilai'):
        return make_response(jsonify({'error': 'periode nilai diperlukan!'}), 400)
    if not params.get('id_mapel'):
        return make_response(jsonify({'error': 'ID Mapel diperlukan!'}), 400)
    if not params.get('nilai'):
        return make_response(jsonify({'error': 'Nilai diperlukan!'}), 400)
    # Add to DB
    schema = RaporNilaiSchema()
    query = schema.load(params)
    db.session.add(query)
    db.session.commit()
    # Make JSON Response
    response = schema.dump(query)
    return make_response(jsonify({'message': 'success', 'data': response}), 201)