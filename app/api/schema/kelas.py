from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from api.models import Kelas
from .jurusan import JurusanSchema
from api import db

class KelasSchema(SQLAlchemySchema):
    class Meta:
        model = Kelas
        sqla_session = db.session
        load_instance = True
    
    id_kelas = auto_field(dump_only=True)
    jenjang_kelas = auto_field()
    urutan_kelas = auto_field()
    jurusan = Nested(JurusanSchema, only=['nama_jurusan'], dump_only=True)
    id_jurusan = auto_field(load_only=True)
    wali_kelas = auto_field()
    reg_date = auto_field(dump_only=True)