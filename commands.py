import click
import json
from flask.cli import with_appcontext
from extenstions import db
from flask import current_app
from record.models import OfferedServices, ManufacturedProduct, Accreditation, SterileLiquide, SterileLyophilized, \
    NonSterileLiquide, NonSterileSolid, NonSterileSemiSolid, PrimaryPackaging, SecondaryPackaging

files = ["accreditations", "manufactured_product_type", "offered_services", "sterile_liquide", "sterile_lyophilized",
         "non_sterile_liquide", "non_sterile_solid", "non_sterile_semi_solid", "primary_packaging",
         "secondary_packaging"]


def is_in_db(resource, condition):
    return resource.query.filter(condition).first()


@click.command(name="initialize_data")
@with_appcontext
def initialize_data():
    with db.engine.connect():
        path = current_app.config.get("DATA_SAMPLE_PATH")
        for file_name in files:
            with open(path + f"/{file_name}.json") as f:
                data = json.load(f)
                for item in data:
                    if file_name == "accreditations":
                        acc = is_in_db(resource=Accreditation,
                                       condition=((Accreditation.accreditation_name == item.get("accreditation_name"))))
                        if acc:
                            continue
                        acc = Accreditation(accreditation_name=item.get("accreditation_name"))
                        db.session.add(acc)
                        db.session.commit()
                    elif file_name == "manufactured_product_type":
                        product_type = is_in_db(ManufacturedProduct, condition=(
                        (ManufacturedProduct.product_name == item.get("product_name"))))
                        if product_type:
                            continue
                        product_type = ManufacturedProduct(product_name=item.get("product_name"))
                        db.session.add(product_type)
                        db.session.commit()
                    elif file_name == "offered_services":
                        service = is_in_db(OfferedServices,
                                           condition=((OfferedServices.service_name == item.get("service_name"))))
                        if service:
                            continue
                        service = OfferedServices(service_name=item.get("service_name"))
                        db.session.add(service)
                        db.session.commit()
                    elif file_name == "sterile_liquide":
                        ste_liq = is_in_db(SterileLiquide, condition=(
                        (SterileLiquide.sterile_liq_name == item.get("sterile_liq_name"))))

                        if ste_liq:
                            continue
                        ste_liq = SterileLiquide(sterile_liq_name=item.get("sterile_liq_name"))
                        db.session.add(ste_liq)
                        db.session.commit()
                    elif file_name == "sterile_lyophilized":
                        ste_liq = is_in_db(SterileLyophilized, condition=(
                        (SterileLyophilized.lyophilized_name == item.get("lyophilized_name"))))

                        if ste_liq:
                            continue
                        ste_liq = SterileLyophilized(lyophilized_name=item.get("lyophilized_name"))
                        db.session.add(ste_liq)
                        db.session.commit()
                    elif file_name == "non_sterile_liquide":
                        ste_liq = is_in_db(NonSterileLiquide,
                                           condition=((NonSterileLiquide.liquide_name == item.get("liquide_name"))))
                        if ste_liq:
                            continue
                        ste_liq = NonSterileLiquide(liquide_name=item.get("liquide_name"))
                        db.session.add(ste_liq)
                        db.session.commit()
                    elif file_name == "non_sterile_solid":
                        ste_liq = is_in_db(NonSterileSolid,
                                           condition=((NonSterileSolid.solid_name == item.get("solid_name"))))
                        if ste_liq:
                            continue
                        ste_liq = NonSterileSolid(solid_name=item.get("solid_name"))
                        db.session.add(ste_liq)
                        db.session.commit()

                    elif file_name == "non_sterile_semi_solid":
                        ste_liq = is_in_db(NonSterileSemiSolid, condition=(
                        (NonSterileSemiSolid.semi_solid_name == item.get("semi_solid_name"))))

                        if ste_liq:
                            continue
                        ste_liq = NonSterileSemiSolid(semi_solid_name=item.get("semi_solid_name"))
                        db.session.add(ste_liq)
                        db.session.commit()

                    elif file_name == "primary_packaging":
                        ste_liq = is_in_db(PrimaryPackaging, condition=(
                        (PrimaryPackaging.pri_packaging_name == item.get("pri_packaging_name"))))

                        if ste_liq:
                            continue
                        ste_liq = PrimaryPackaging(pri_packaging_name=item.get("pri_packaging_name"))
                        db.session.add(ste_liq)
                        db.session.commit()

                    elif file_name == "secondary_packaging":
                        ste_liq = is_in_db(SecondaryPackaging, condition=(
                        (SecondaryPackaging.sec_packaging_name == item.get("sec_packaging_name"))))

                        if ste_liq:
                            continue
                        ste_liq = SecondaryPackaging(sec_packaging_name=item.get("sec_packaging_name"))
                        db.session.add(ste_liq)
                        db.session.commit()
