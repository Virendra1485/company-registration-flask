import enum
from extenstions import db, bcrypt, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import redirect, url_for, flash


@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'warning')
    return redirect(url_for('/.login'))


class CountryChoice(enum.Enum):
    INDIA = "India"
    RUSSIA = "Russia"


def get_enum_by_value(enum_class, value):
    for enum_member in enum_class:
        if enum_member.value == value:
            return enum_member
    raise ValueError(f"No enum member with value '{value}' found in {enum_class.__name__}")

class Company(db.Model, UserMixin):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(220))
    email = db.Column(db.String(220), unique=True)
    password_hash = db.Column(db.String(220))

    def __init__(self, email, password, company_name):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password.strip()).decode('utf-8')
        # self.password_hash = generate_password_hash(password)
        self.company_name = company_name

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


company_offered_services = db.Table(
    'company_offered_services',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('offered_service_id', db.Integer, db.ForeignKey('offered_services.id'), primary_key=True)
)

company_manufacture_product = db.Table(
    'company_manufacture_product',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('manufactured_products_id', db.Integer, db.ForeignKey('manufactured_products.id'), primary_key=True)
)

company_accreditation = db.Table(
    'company_accreditation',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('accreditations_id', db.Integer, db.ForeignKey('accreditations.id'), primary_key=True)
)

company_sterile_liquide = db.Table(
    'company_sterile_liquide',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('ste_liq_id', db.Integer, db.ForeignKey('bulk_prod_ste_liq.id'), primary_key=True)
)

company_ste_lyo = db.Table(
    'company_sterile_lyophilized',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('ste_lyo_id', db.Integer, db.ForeignKey('bulk_prod_ste_lyo.id'), primary_key=True)
)

company_non_ste_liq = db.Table(
    'company_non_ste_liq',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('non_ste_lyo_id', db.Integer, db.ForeignKey('bulk_prod_non_ste_liq.id'), primary_key=True)
)

company_non_sterile_solid = db.Table(
    'company_non_ste_solid',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('non_ste_solid_id', db.Integer, db.ForeignKey('bulk_prod_non_ste_solid.id'), primary_key=True)
)

company_non_ste_semi_solid = db.Table(
    'company_non_ste_semi_solid',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('non_ste_semi_solid_id', db.Integer, db.ForeignKey('bulk_prod_non_ste_semi_solid.id'), primary_key=True)
)

company_primary_packaging = db.Table(
    'company_primary_packaging',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('pri_packaging_id', db.Integer, db.ForeignKey('primary_packaging.id'), primary_key=True)
)

company_secondary_packaging = db.Table(
    'company_secondary_packaging',
    db.Column('company_id', db.Integer, db.ForeignKey('company_details.id'), primary_key=True),
    db.Column('sec_packaging_id', db.Integer, db.ForeignKey('secondary_packaging.id'), primary_key=True)
)


class CompanyDetails(db.Model):
    __tablename__ = "company_details"

    id = db.Column(db.Integer, primary_key=True)
    cmo = db.Column(db.String(220), nullable=False)
    manufacturing_site = db.Column(db.String(220), nullable=False)
    address = db.Column(db.String(220), nullable=False)
    country = db.Column(db.Enum(CountryChoice), nullable=False)

    offered_choice = db.relationship('OfferedServices', secondary='company_offered_services',
                                     backref=db.backref('offered_service'), lazy='dynamic')

    manufactured_product_type = db.relationship('ManufacturedProduct', secondary='company_manufacture_product',
                                                backref=db.backref('manufactured_products'), lazy='dynamic')

    accreditations = db.relationship('Accreditation', secondary='company_accreditation',
                                     backref=db.backref('manufactured_products'), lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    sterile_liquide = db.relationship('SterileLiquide', secondary='company_sterile_liquide',
                                      backref=db.backref('company_sterile_liquide'), lazy='dynamic')
    sterile_lyophilized = db.relationship('SterileLyophilized', secondary='company_sterile_lyophilized',
                                          backref=db.backref('company_sterile_lyophilized'), lazy='dynamic')
    non_sterile_liquide = db.relationship('NonSterileLiquide', secondary='company_non_ste_liq',
                                          backref=db.backref('company_non_ste_liq'), lazy='dynamic')
    non_sterile_solid = db.relationship('NonSterileSolid', secondary='company_non_ste_solid',
                                        backref=db.backref('company_non_ste_solid'), lazy='dynamic')
    non_sterile_semi_solid = db.relationship('NonSterileSemiSolid', secondary='company_non_ste_semi_solid',
                                             backref=db.backref('company_non_ste_semi_solid'), lazy='dynamic')
    primary_packaging = db.relationship('PrimaryPackaging', secondary='company_primary_packaging',
                                        backref=db.backref('company_primary_packaging'), lazy='dynamic')
    secondary_packaging = db.relationship('SecondaryPackaging', secondary='company_secondary_packaging',
                                          backref=db.backref('company_secondary_packaging'), lazy='dynamic')


class OfferedServices(db.Model):
    __tablename__ = "offered_services"

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(220), nullable=False)


class ManufacturedProduct(db.Model):
    __tablename__ = "manufactured_products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(220), nullable=False)


class Accreditation(db.Model):
    __tablename__ = "accreditations"

    id = db.Column(db.Integer, primary_key=True)
    accreditation_name = db.Column(db.String(220), nullable=False)


class SterileLiquide(db.Model):
    __tablename__ = "bulk_prod_ste_liq"

    id = db.Column(db.Integer, primary_key=True)
    sterile_liq_name = db.Column(db.String(220), nullable=False)


class SterileLyophilized(db.Model):
    __tablename__ = "bulk_prod_ste_lyo"

    id = db.Column(db.Integer, primary_key=True)
    lyophilized_name = db.Column(db.String(220), nullable=False)


class NonSterileLiquide(db.Model):
    __tablename__ = "bulk_prod_non_ste_liq"

    id = db.Column(db.Integer, primary_key=True)
    liquide_name = db.Column(db.String(220), nullable=False)


class NonSterileSolid(db.Model):
    __tablename__ = "bulk_prod_non_ste_solid"

    id = db.Column(db.Integer, primary_key=True)
    solid_name = db.Column(db.String(220), nullable=False)


class NonSterileSemiSolid(db.Model):
    __tablename__ = "bulk_prod_non_ste_semi_solid"

    id = db.Column(db.Integer, primary_key=True)
    semi_solid_name = db.Column(db.String(220), nullable=False)


class PrimaryPackaging(db.Model):
    __tablename__ = "primary_packaging"

    id = db.Column(db.Integer, primary_key=True)
    pri_packaging_name = db.Column(db.String(220), nullable=False)


class SecondaryPackaging(db.Model):
    __tablename__ = "secondary_packaging"

    id = db.Column(db.Integer, primary_key=True)
    sec_packaging_name = db.Column(db.String(220), nullable=False)
