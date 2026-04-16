# het hoofdbestand, hierin draait Flask en staan alle routes

from flask import Flask, render_template, redirect, url_for, request
from extensions import db
from models import Taak, Categorie
from forms import TaakForm, CategorieForm
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
# Maakt de webapplicatie aan:
app = Flask(__name__)

# Koppelt de database (drie schuine strepen = huidige map):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taken.db'
app.config['SECRET_KEY'] = 'geheime-sleutel'
db.init_app(app)


@app.route('/', methods=['GET'])    # Hoofdpagina met links naar de rest
def index():
    return render_template('index.html')


@app.route('/overzicht', methods=['GET'])   # Toont alle taken uit de database
def overzicht():
    taken = Taak.query.all()
    return render_template('overzicht.html', taken=taken)


@app.route('/taak/toevoegen', methods=['GET', 'POST'])  # GET = formulier tonen, POST = formulier verwerken
def taak_toevoegen():
    form = TaakForm()
    categorieën = Categorie.query.all()

    # Vult het dropdown menu met categorieën, of geeft een melding als er nog geen zijn:
    if categorieën:
        form.categorie.choices = [(c.id, c.naam) for c in categorieën]
    else:
        form.categorie.choices = [(0, 'Nog geen categorieën!')]

    if form.validate_on_submit():
        nieuwe_taak = Taak(
            titel=form.titel.data,
            beschrijving=form.beschrijving.data,
            categorie_id=form.categorie.data if categorieën else None  # Sla geen ongeldige categorie op
        )
        db.session.add(nieuwe_taak)
        db.session.commit()
        return redirect(url_for('overzicht'))

    return render_template('taak_toevoegen.html', form=form)


@app.route('/taak/verwijderen/<int:taak_id>', methods=['POST'])     # Verwijdert een taak op basis van zijn ID
def taak_verwijderen(taak_id):
    taak = Taak.query.get_or_404(taak_id)   # Geeft een 404-fout als de taak niet bestaat
    db.session.delete(taak)
    db.session.commit()
    return redirect(url_for('overzicht'))


@app.route('/taak/afgerond/<int:taak_id>', methods=['POST'])    # Markeert een taak als afgerond of niet afgerond
def taak_afgerond(taak_id):
    taak = Taak.query.get_or_404(taak_id)
    taak.afgerond = not taak.afgerond   # Wisselt tussen True en False
    db.session.commit()
    return redirect(url_for('overzicht'))


@app.route('/categorie/toevoegen', methods=['GET', 'POST'])     # GET = formulier tonen, POST = formulier verwerken
def categorie_toevoegen():
    categorie_form = CategorieForm()
    if categorie_form.validate_on_submit():
        nieuwe_categorie = Categorie(
            naam=categorie_form.naam.data,
            beschrijving=categorie_form.beschrijving.data
        )
        db.session.add(nieuwe_categorie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('categorie_toevoegen.html', categorie_form=categorie_form)


@app.route('/categorie/verwijderen/<int:categorie_id>', methods=['POST'])   # Verwijdert een categorie op basis van zijn ID
def categorie_verwijderen(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)    # Geeft een 404-fout als de categorie niet bestaat

    # Koppel taken los van deze categorie voordat de categorie wordt verwijderd:
    for taak in categorie.taken:
        taak.categorie_id = None

    db.session.delete(categorie)
    db.session.commit()
    return redirect(url_for('categorie_overzicht'))


@app.route('/categorie/overzicht', methods=['GET'])     # Toont alle categorieën uit de database
def categorie_overzicht():
    categorieën = Categorie.query.all()
    return render_template('categorie_overzicht.html', categorieën=categorieën)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()     # Maakt alle tabellen aan als ze nog niet bestaan
    app.run(debug=True)     # Start de Flask-ontwikkelserver (herlaadt automatisch bij codewijzigingen)
