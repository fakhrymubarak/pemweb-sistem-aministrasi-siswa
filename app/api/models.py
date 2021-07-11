# coding: utf-8
from . import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Admin(db.Model):
    __tablename__ = 'admin'

    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    reg_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_pasword(self, password):
        return check_password_hash(self.password, password)



class Guru(db.Model):
    __tablename__ = 'guru'

    id_guru = db.Column(db.Integer, primary_key=True)
    nama_guru = db.Column(db.String(50), nullable=False)
    nip = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    isWaliKelas = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    reg_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_pasword(self, password):
        return check_password_hash(self.password, password)


class Jurusan(db.Model):
    __tablename__ = 'jurusan'

    id_jurusan = db.Column(db.Integer, primary_key=True)
    nama_jurusan = db.Column(db.String(20))



class Kelas(db.Model):
    __tablename__ = 'kelas'

    id_kelas = db.Column(db.Integer, primary_key=True)
    reg_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    jenjang_kelas = db.Column(db.String(3), nullable=False)
    urutan_kelas = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    id_jurusan = db.Column(db.ForeignKey('jurusan.id_jurusan'), nullable=False, index=True)
    wali_kelas = db.Column(db.ForeignKey('guru.id_guru'), nullable=False, index=True)

    jurusan = db.relationship('Jurusan', primaryjoin='Kelas.id_jurusan == Jurusan.id_jurusan', backref='kelas')
    guru = db.relationship('Guru', primaryjoin='Kelas.wali_kelas == Guru.id_guru', backref='kelas')



class Mapel(db.Model):
    __tablename__ = 'mapel'

    id_mapel = db.Column(db.Integer, primary_key=True)
    nama_mapel = db.Column(db.String(50), nullable=False)
    id_jurusan = db.Column(db.ForeignKey('jurusan.id_jurusan'), nullable=False, index=True)
    reg_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    jurusan = db.relationship('Jurusan', primaryjoin='Mapel.id_jurusan == Jurusan.id_jurusan', backref='mapels')



class PeriodeAjaran(db.Model):
    __tablename__ = 'periode_ajaran'
    __table_args__ = (
        db.Index('unik', 'tahun_ajaran', 'semester'),
    )

    id = db.Column(db.SmallInteger, primary_key=True)
    tahun_ajaran = db.Column(db.String(9), nullable=False)
    semester = db.Column(db.Enum('Ganjil', 'Genap'), nullable=False)



class RaporNilai(db.Model):
    __tablename__ = 'rapor_nilai'

    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.ForeignKey('siswa.nis'), nullable=False, index=True)
    id_mapel = db.Column(db.ForeignKey('mapel.id_mapel'), nullable=False, index=True)
    nilai = db.Column(db.Integer)
    periode_nilai = db.Column(db.ForeignKey('periode_ajaran.id'), nullable=False, index=True)

    mapel = db.relationship('Mapel', primaryjoin='RaporNilai.id_mapel == Mapel.id_mapel', backref='rapor_nilais')
    siswa = db.relationship('Siswa', primaryjoin='RaporNilai.nis == Siswa.nis', backref='rapor_nilais')
    periode_ajaran = db.relationship('PeriodeAjaran', primaryjoin='RaporNilai.periode_nilai == PeriodeAjaran.id', backref='rapor_nilais')



class Siswa(db.Model):
    __tablename__ = 'siswa'

    nis = db.Column(db.String(10), primary_key=True)
    nama_siswa = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    jenkel = db.Column(db.Enum('L', 'P'), nullable=False)
    id_kelas = db.Column(db.ForeignKey('kelas.id_kelas'), nullable=False, index=True)
    isActive = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    reg_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    kelas = db.relationship('Kelas', primaryjoin='Siswa.id_kelas == Kelas.id_kelas', backref='siswas')
