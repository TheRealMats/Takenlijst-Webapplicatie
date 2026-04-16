# hierin beschrijven we hoe de database eruitziet, dus wat een "taak" en "categorie" precies is

from extensions import db

# De eerste tabel heet Taak:
class Taak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(50), nullable=False)
    beschrijving = db.Column(db.String(500), nullable=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=True)  # Verwijst naar de id in de categorietabel
    afgerond = db.Column(db.Boolean, default=False)     # Nieuwe taak is standaard niet afgerond
    categorie = db.relationship('Categorie', back_populates='taken')    # Directe relatie met Categorie zodat je taak.categorie.naam kunt gebruiken

# De tweede tabel heet Categorie:
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    beschrijving = db.Column(db.String(500), nullable=True)
    taken = db.relationship('Taak', back_populates='categorie')     # Hiermee kun je vanuit een categorie alle bijbehorende taken ophalen via categorie.taken

