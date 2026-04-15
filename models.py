# hierin beschrijven we hoe de database eruitziet, dus wat een "taak" precies is (titel, datum, afgevinkt of niet)

from extensions import db

# De eerste tabel heet Taak en wordt geconfigureert (aangemaakt) door Model van SQLAlchemy. Ook wordt deze gekoppeld aan de databbase:
class Taak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(50), nullable=False)
    beschrijving = db.Column(db.String(500), nullable=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=True)  # *Koppeling* die zegt: "dit getal verwijst naar de rij id in de categorietabel". De foreign key zorgt dat elke taak weet bij welke categorie hij hoort. En ja, het moet 'categorie' zijn, niet 'Categorie', want hij koppelt met SQLAlchemy aan tabelnaam, niet klassenaam!
    afgerond = db.Column(db.Boolean, default=False)     # nieuwe taak standaard niet afgerond als je hem aanmaakt.
    categorie = db.relationship('Categorie')    # Voegt rechtstreeks een relatie toe met de tabel Categorie zodat ik dit over kan nemen in html voor het overzicht!

# De tweede tabel heet Categorie en werkt om categorien op te kunnen slaan:
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(50), nullable=False)
    beschrijving = db.Column(db.String(500), nullable=True)
    # Mogelijke om (later) toe te voegen: "taken = db.relationship('Taak', backref='categorie')". Dit is een relatie die zorgt dat je vanuit een categorie alle bijbehorende taken kunt ophalen, en andersom met de backref regel. 'Taak' verwijst naar de klasse Taak!
