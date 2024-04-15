from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CompanyForm, CompanyRegistrationForm, LogInForm
from flask.views import MethodView
from .models import Company, CompanyDetails, ManufacturedProduct, OfferedServices, Accreditation, SterileLiquide, \
    SterileLyophilized, NonSterileLiquide, NonSterileSolid, NonSterileSemiSolid, PrimaryPackaging, SecondaryPackaging
from extenstions import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user

record_route = Blueprint("/", __name__, )


# @record_route.route("/", methods=['GET', 'POST'])
# def record():
#     form = CompanyForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         # Process the form data and create a new Company object
#         # Save the new Company object to the database
#         return 'Company created successfully'
#     return render_template('company_list_page.html', form=form)


class AdminRegistration(MethodView):
    def __init__(self):
        self.form = CompanyRegistrationForm()

    def get(self):
        return render_template('company_registration.html', form=self.form)

    def post(self):
        if self.form.validate_on_submit():
            detail_entry = Company(company_name=self.form.company_name.data, email=self.form.email.data.strip(),
                                   password=self.form.password.data)
            db.session.add(detail_entry)
            db.session.commit()
            return redirect(url_for('/.login'))
        return render_template('company_registration.html', form=self.form)


record_route.add_url_rule('/registration', view_func=AdminRegistration.as_view('registration'),
                          methods=['GET', 'POST'])


class CompanyLogin(MethodView):
    def get(self):
        form = LogInForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LogInForm()
        if form.validate_on_submit():
            company = Company.query.filter_by(email=form.email.data.strip()).first()
            if company and company.check_password(form.password.data.strip()):
                login_user(company)
                flash('Login Successful!!', 'success')
                return redirect(url_for('/.record'))
            else:
                flash('Invalid Email Id or Password', 'danger')
        return render_template('login.html', form=form)


record_route.add_url_rule('/login', view_func=CompanyLogin.as_view('login'), methods=['GET', 'POST'])


@record_route.route('/logout')
@login_required  # Ensure the user is logged in before accessing this route
def logout():
    logout_user()  # Logout the current user
    flash('You have been logged out', 'success')
    return redirect(url_for('/.login'))


class RecordView(MethodView):
    decorators = [login_required]

    def get(self):
        company_details = CompanyDetails.query.filter_by(company_id=current_user.id).order_by(CompanyDetails.id).all()
        services = OfferedServices.query.all()
        prod_types = ManufacturedProduct.query.all()
        accreditation = Accreditation.query.all()
        sterile_liquide = SterileLiquide.query.all()
        all_sterile_lyophilized = SterileLyophilized.query.all()
        all_non_sterile_liquides = NonSterileLiquide.query.all()
        all_non_sterile_solids = NonSterileSolid.query.all()
        all_non_sterile_semi_solid = NonSterileSemiSolid.query.all()
        all_primary_packaging = PrimaryPackaging.query.all()
        all_secondary_packaging = SecondaryPackaging.query.all()

        return render_template('basic.html',
                               context={"details": company_details, "all_accreditations": accreditation,
                                        "services": services, "prod_types": prod_types,
                                        "all_sterile_liquides": sterile_liquide,
                                        "all_sterile_lyophilized": all_sterile_lyophilized,
                                        "all_non_sterile_solids": all_non_sterile_solids,
                                        "all_non_sterile_liquides": all_non_sterile_liquides,
                                        "all_non_sterile_semi_solid": all_non_sterile_semi_solid,
                                        "all_primary_packaging": all_primary_packaging,
                                        "all_secondary_packaging": all_secondary_packaging,
                                        "error": request.args.get("error")}, form=CompanyForm())

    def post(self):
        form = CompanyForm(request.form)
        if form.validate():
            company_detail = CompanyDetails(cmo=form.cmo.data, manufacturing_site=form.manufacturing_site.data,
                                            address=form.address.data, country=form.country.data,
                                            company_id=current_user.id)

            db.session.add(company_detail)
            db.session.commit()
            company_detail.manufactured_product_type = ManufacturedProduct.query.filter(
                ManufacturedProduct.id.in_(form.manufactured_product_type.data)).all()
            company_detail.offered_choice = OfferedServices.query.filter(
                OfferedServices.id.in_(form.offered_choice.data)).all()
            company_detail.accreditations = Accreditation.query.filter(
                Accreditation.id.in_(form.accreditations.data)).all()
            company_detail.sterile_liquide = SterileLiquide.query.filter(
                SterileLiquide.id.in_(form.sterile_liquide.data)).all()
            company_detail.sterile_lyophilized = SterileLyophilized.query.filter(
                SterileLyophilized.id.in_(form.sterile_lyophilized.data)).all()
            company_detail.non_sterile_solid = NonSterileSolid.query.filter(
                NonSterileSolid.id.in_(form.non_sterile_solid.data)).all()
            company_detail.non_sterile_liquide = NonSterileLiquide.query.filter(
                NonSterileLiquide.id.in_(form.non_sterile_liquid.data)).all()
            company_detail.non_sterile_semi_solid = NonSterileSemiSolid.query.filter(
                NonSterileSemiSolid.id.in_(form.non_sterile_semi_solid.data)).all()
            company_detail.primary_packaging = PrimaryPackaging.query.filter(
                NonSterileSemiSolid.id.in_(form.primary_packaging.data)).all()
            company_detail.secondary_packaging = SecondaryPackaging.query.filter(
                SecondaryPackaging.id.in_(form.secondary_packaging.data)).all()
            db.session.commit()
            return redirect(url_for("/.record"))
        return redirect(url_for("/.record"))


record_route.add_url_rule('/', view_func=RecordView.as_view('record'))


@record_route.route('/update_company/<int:company_id>', methods=['GET', 'POST'])
def update_company_details(company_id):
    company = CompanyDetails.query.get_or_404(company_id)
    form = CompanyForm(obj=company)
    if form.validate():
        company.cmo = form.cmo.data
        company.manufacturing_site = form.manufacturing_site.data
        company.address = form.address.data
        breakpoint()
        company.country = form.country.data
        company.offered_choice = OfferedServices.query.filter(OfferedServices.id.in_(form.offered_choice.data)).all()
        company.manufactured_product_type = ManufacturedProduct.query.filter(
            ManufacturedProduct.id.in_(form.manufactured_product_type.data)).all()
        company.accreditations = Accreditation.query.filter(Accreditation.id.in_(form.accreditations.data)).all()
        company.sterile_liquide = SterileLiquide.query.filter(SterileLiquide.id.in_(form.sterile_liquide.data)).all()
        company.sterile_lyophilized = SterileLyophilized.query.filter(
            SterileLyophilized.id.in_(form.sterile_lyophilized.data)).all()
        company.non_sterile_liquide = NonSterileLiquide.query.filter(
            NonSterileLiquide.id.in_(form.non_sterile_liquid.data)).all()
        company.non_sterile_solid = NonSterileSolid.query.filter(
            NonSterileSolid.id.in_(form.non_sterile_solid.data)).all()
        company.non_sterile_semi_solid = NonSterileSemiSolid.query.filter(
            NonSterileSemiSolid.id.in_(form.non_sterile_semi_solid.data)).all()
        company.primary_packaging = PrimaryPackaging.query.filter(
            PrimaryPackaging.id.in_(form.primary_packaging.data)).all()
        company.secondary_packaging = SecondaryPackaging.query.filter(
            SecondaryPackaging.id.in_(form.secondary_packaging.data)).all()
        db.session.commit()
        flash('Company details updated successfully!', 'success')
        return redirect(url_for('/.record'))
    return redirect(url_for("/.record", error=form.errors))
