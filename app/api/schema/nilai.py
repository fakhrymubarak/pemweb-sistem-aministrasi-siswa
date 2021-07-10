from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow.fields import Pluck
from api.models import RaporNilai
from .mapel import MapelSchema
from .periode_ajaran import PeriodeAjaranSchema
from api import db

class RaporNilaiSchema(SQLAlchemySchema):
    class Meta:
        model = RaporNilai
        sqla_session = db.session
        load_instance = True
    
    nis = auto_field(load_only=True)
    periode_nilai = auto_field(load_only=True)
    id_mapel = auto_field()
    mapel = Pluck(MapelSchema, 'nama_mapel', dump_only=True)
    nilai = auto_field()