from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, PasswordField, SubmitField, validators, MultipleFileField, \
    SelectMultipleField
from wtforms.validators import InputRequired
from wtforms.widgets import CheckboxInput

from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import CountryChoice, Company, OfferedServices, Accreditation, ManufacturedProduct, SterileLiquide, \
    SterileLyophilized, NonSterileLiquide, NonSterileSolid, NonSterileSemiSolid, PrimaryPackaging, SecondaryPackaging


class CompanyRegistrationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(form, field):
        company = Company.query.filter_by(email=field.data).first()
        if company:
            raise validators.ValidationError('Email already exists. Please use a different email.')


class LogInForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CompanyForm(FlaskForm):
    cmo = StringField('CMO', validators=[InputRequired()])
    manufacturing_site = StringField('Manufacturing Site', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    country = SelectField('Country', choices=[(choice.name, choice.value) for choice in CountryChoice],
                          validators=[InputRequired()])

    offered_choice = SelectMultipleField('Offered Services', coerce=int, validators=[DataRequired()])
    manufactured_product_type = SelectMultipleField('Manufactured Product Type', coerce=int,
                                                    validators=[InputRequired()])
    accreditations = SelectMultipleField('Accreditations', coerce=int, validators=[InputRequired()])
    sterile_liquide = SelectMultipleField('Liquide', coerce=int, validators=[InputRequired()])
    sterile_lyophilized = SelectMultipleField('Lyophilized', coerce=int, validators=[InputRequired()])
    non_sterile_liquid = SelectMultipleField('Liquide', coerce=int, validators=[InputRequired()])
    non_sterile_solid = SelectMultipleField('Solid', coerce=int, validators=[InputRequired()])
    non_sterile_semi_solid = SelectMultipleField('Semi-Solid', coerce=int, validators=[InputRequired()])
    primary_packaging = SelectMultipleField('Primary Packaging', coerce=int, validators=[InputRequired()])
    secondary_packaging = SelectMultipleField('Secondary Packaging', coerce=int, validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.offered_choice.choices = [(service.id, service.service_name) for service in OfferedServices.query.all()]
        self.manufactured_product_type.choices = [(product.id, product.product_name) for product in
                                                  ManufacturedProduct.query.all()]
        self.accreditations.choices = [(accredit.id, accredit.accreditation_name) for accredit in
                                       Accreditation.query.all()]
        self.sterile_liquide.choices = [(ste_liq.id, ste_liq.sterile_liq_name) for ste_liq in
                                        SterileLiquide.query.all()]
        self.sterile_lyophilized.choices = [(ste_lyo.id, ste_lyo.lyophilized_name) for ste_lyo in
                                            SterileLyophilized.query.all()]
        self.non_sterile_liquid.choices = [(non_str_liq.id, non_str_liq.liquide_name) for non_str_liq in
                                           NonSterileLiquide.query.all()]
        self.non_sterile_solid.choices = [(non_str_solid.id, non_str_solid.solid_name) for non_str_solid in
                                          NonSterileSolid.query.all()]
        self.non_sterile_semi_solid.choices = [(non_str_semi_solid.id, non_str_semi_solid.semi_solid_name) for
                                               non_str_semi_solid in NonSterileSemiSolid.query.all()]
        self.primary_packaging.choices = [(pri_pack.id, pri_pack.pri_packaging_name) for pri_pack in
                                          PrimaryPackaging.query.all()]
        self.secondary_packaging.choices = [(sec_pack.id, sec_pack.sec_packaging_name) for sec_pack in
                                            SecondaryPackaging.query.all()]

# class UpdateCompanyDetailsForm(FlaskForm):
#     cmo = StringField('CMO', validators=[InputRequired()])
#     manufacturing_site = StringField('Manufacturing Site', validators=[InputRequired()])
#     address = StringField('Address', validators=[InputRequired()])
#     country = SelectField('Country', choices=[(choice.name, choice.value) for choice in CountryChoice],
#                           validators=[DataRequired()])
#     offered_services = MultipleFileField('Offered Services',
#                                          choices=[(choice.name, choice.value) for choice in ServicesChoice],
#                                          validators=[InputRequired()])
#     manufactured_product_type = RadioField('Manufactured Product Type',
#                                            choices=[(choice.name, choice.value) for choice in ProductChoice],
#                                            validators=[InputRequired()])
#     accreditations = RadioField('Accreditations',
#                                 choices=[(choice.name, choice.value) for choice in AccreditationsChoice],
#                                 validators=[InputRequired()])
#
