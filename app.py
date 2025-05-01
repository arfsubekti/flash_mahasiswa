import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup database path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'mahasiswa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    npm = db.Column(db.String(20), unique=True, nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('daftar_mahasiswa'))

@app.route('/tambah', methods=['GET', 'POST'])
def form_tambah_mahasiswa():
    if request.method == 'POST':
        nama = request.form['nama']
        npm = request.form['npm']
        jurusan = request.form['jurusan']
        mahasiswa = Mahasiswa(nama=nama, npm=npm, jurusan=jurusan)
        db.session.add(mahasiswa)
        db.session.commit()
        return redirect(url_for('daftar_mahasiswa'))
    return render_template('form_tambah_mahasiswa.html')

@app.route('/daftar')
def daftar_mahasiswa():
    data = Mahasiswa.query.all()
    return render_template('daftar_mahasiswa.html', mahasiswa=data)

if __name__ == '__main__':
    # Pastikan folder instance ada
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

    # Buat tabel
    with app.app_context():
        db.create_all()

    app.run(debug=True)
