# hierin staan de formulieren, dus bijvoorbeeld het formulier om een taak toe te voegen

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

# VCoor nu hebben we maar één simpel formulier nodig: dat om een taak toe te voegen! Er kan mogelijk later nog meer aan toegevoegd worden, bijvoorbeeld als we meerdere categorien krijgen.

class TaakForm(FlaskForm):
    titel = StringField('Taak', validators=[DataRequired()])
    beschrijving = StringField('Beschrijving van taak')
    categorie = SelectField('Categorie', coerce=int)    # coerce=int zorgt dat de gekozen waarde wordt omgezet naar een (geheel) getal. Dat is nodig omdat de id van een categorie een getal is, maar een formulier alles standaard als tekst verstuurt. coerce betekent: "Omzetten naar een ander type".
    submit = SubmitField('Taak toevoegen')

class CategorieForm(FlaskForm):
    naam = StringField('Categorie', validators=[DataRequired()])
    beschrijving = StringField('Beschijving van categorie')
    submit = SubmitField('Categorie toevoegen')