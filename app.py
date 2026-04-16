# het hoofdbestand, hierin draait Flask en staan alle routes (zoals / en /toevoegen)

# Eventjes de hoofd-libraries toevoegen:
from flask import Flask, render_template, redirect, url_for, request   # request houdt bij wat browser op bepaald moment naar server stuurt (methode en data, etc)
from extensions import db
from models import Taak, Categorie
from forms import TaakForm, CategorieForm

# Maakt de webapplicatie aan:
app = Flask(__name__)

# Maakt en koppelt de database. Dit zet hij ook gelijk in de goede projectmap via de drie schuine strepen (betekent: "in huidige map"):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taken.db'
app.config['SECRET_KEY'] = 'geheime-sleutel'
db.init_app(app)

@app.route('/', methods=['GET'])    # Dit is de hoofdpagina: hoeft alleen GET
def index():
    return render_template('index.html')

@app.route('/overzicht', methods=['GET'])    # Laadt alleen alle taken uit de tabel: Taak
def overzicht():
    taken = Taak.query.all()
    return render_template('overzicht.html', taken=taken)

@app.route('/taak/toevoegen', methods=['GET', 'POST'])    # Verwerkt het taakformulier en voegt aan de taak-tabel toe: GET = pagina ophalen en tonen; POST = formulier versturen en verwerken
def taak_toevoegen():
    form = TaakForm()
    categorieën = Categorie.query.all()  # Dit laat weer gwn de keuzes voor de categorie (dropdown) binnen het formulier zien, maar houdt er ook rekening mee als er niets is.
    if categorieën:     # Heb dit even aangepast want anders komt er een crash als er geen categorien zijn...
        form.categorie.choices = [(c.id, c.naam) for c in categorieën]
    else:
        form.categorie.choices = [(0, 'Nog geen categorieen!')]   
    if request.method == 'POST' and form.validate_on_submit():
            nieuwe_taak = Taak(
                titel=form.titel.data,
                beschrijving=form.beschrijving.data,
                categorie_id=form.categorie.data
            )
            db.session.add(nieuwe_taak)
            db.session.commit()
            return redirect(url_for('overzicht'))
    return render_template('taak_toevoegen.html', form=form)    # Deze wordt altijd eerst uitgevoerd onder GEt!

@app.route('/categorie/toevoegen', methods=['GET', 'POST'])    # Verwerkt het categorieformulier en voegt aan de categorie-tabel toe.
def categorie_toevoegen():
    categorie_form = CategorieForm()
    if request.method == 'POST'and categorie_form.validate_on_submit():
        nieuwe_categorie = Categorie(naam=categorie_form.naam.data, beschrijving=categorie_form.beschrijving.data)
        db.session.add(nieuwe_categorie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('categorie_toevoegen.html', categorie_form=categorie_form)

@app.route('/taak/verwijderen/<int:taak_id>', methods=['POST'])    # Verwijdert een taak op basis van zijn ID
def taak_verwijderen(taak_id):
    taak = Taak.query.get_or_404(taak_id)   # Zoekt de taak op, geeft 404 als hij niet bestaat
    db.session.delete(taak)
    db.session.commit()
    return redirect(url_for('overzicht'))

@app.route('/categorie/verwijderen/<int:categorie_id>', methods=['POST'])    # Verwijdert een categorie op basis van zijn ID
def categorie_verwijderen(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)    # Zoekt de categorie op, geeft 404 als hij niet bestaat
    db.session.delete(categorie)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()     # Maakt alle tabellen aan als ze nog niet bestaan
    app.run(debug=True)     # Start de Flask-ontwikkelserver

