import json
from unidecode import unidecode

from django.template.defaultfilters import slugify, linebreaks
from django.db import transaction
from django.core.management.base import BaseCommand

from signali_taxonomy.models import Category, Keyword
from signali_location.models import Area, AreaSize
from signali_contact.models import ContactPoint, Organisation

def clean(value, capitalize=True):
    value = value.strip()
    if value == '':
        return None
    return value if not capitalize else value[0].upper() + value[1:]

class Command(BaseCommand):
    help = 'Run to import data from JSON-based research tool'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str, choices=['category', 'keyword', 'area', 'point'])
        parser.add_argument('dump', type=str)

    def handle(self, *args, **options):
        with transaction.atomic(), open(options["dump"]) as dump:
            dump = json.load(dump)

            if options['type'] == 'category':
                for entry in dump:
                    parent_category, category = entry["title"].split(':', 1)
                    parent_category = clean(parent_category)
                    category = clean(category)
                    parent_category, is_new = Category.objects.get_or_create(title=parent_category, defaults={
                        'is_public': True
                    })
                    category, is_new = Category.objects.get_or_create(title=category, defaults={
                        'parent': parent_category,
                        'is_public': True
                    })

            if options['type'] == 'keyword':
                for entry in dump:
                    keyword = clean(entry["title"])
                    keyword, is_new = Keyword.objects.get_or_create(title=keyword, defaults={
                        'is_public': True
                    })

            if options['type'] == 'area':
                areasize, is_new = AreaSize.objects.get_or_create(title="Община")
                for entry in dump:
                    area = clean(entry["name"])
                    area, is_new = Area.objects.get_or_create(title=area, defaults={
                        'size': areasize,
                        'is_public': True
                    })

            if options['type'] == 'point':
                area, is_new = Area.objects.get_or_create(title="Национална")
                for entry in dump:
                    point = ContactPoint()
                    point.is_public = True

                    organisation = clean(entry["institution"])
                    organisation = organisation[0].upper() + organisation[1:]
                    organisation, is_new = Organisation.objects.get_or_create(title=organisation)
                    point.organisation = organisation

                    category = clean(entry["category"].split(':')[1])
                    category = Category.objects.get(title=category)
                    point.category = category

                    point.operational_area = area

                    point.save()
                    for tag in entry["tags"]:
                        tag = clean(tag)
                        if tag is None:
                            continue
                        keyword, is_new = Keyword.objects.get_or_create(title=tag)
                        point.keywords.add(keyword)

                    point.title = organisation.title
                    point.slug = slugify(unidecode(point.title))
                    if "email" in entry:
                        point.email = clean(entry["email"], False)
                    if "url" in entry:
                        point.url = clean(entry["url"], False)
                    if "notes" in entry:
                        point.description = linebreaks(clean(entry["notes"], False))

                    if "i18n" in entry:
                        point.is_multilingual = entry["i18n"]
                    if "answerGuarantee" in entry:
                        point.is_response_guaranteed = entry["answerGuarantee"]
                    if "anonimity" in entry:
                        point.is_anonymous_allowed = entry["anonimity"]
                    if "verification" in entry:
                        point.is_verifiable = entry["verification"]
                    if "confirmation" in entry:
                        point.is_confirmation_issued = entry["confirmation"]
                    if "responsive" in entry:
                        point.is_mobile_friendly = entry["responsive"]
                    if "middleMan" in entry:
                        point.is_final_destination = entry["middleMan"]

                    point.is_registration_required = entry["requirements"]["registration"]
                    point.is_photo_required = entry["requirements"]["photo"]
                    point.is_esign_required = entry["requirements"]["esignature"]
                    point.is_name_required = entry["requirements"]["name"]
                    point.is_email_required = entry["requirements"]["email"]
                    point.is_pic_required = entry["requirements"]["egn"]
                    point.is_address_required = entry["requirements"]["address"]
                    point.is_location_required = entry["requirements"]["location"]
                    try:
                        point.is_phone_required = entry["requirements"]["tel"]
                    except:
                        point.is_phone_required = False
                    try:
                        point.is_other_required = entry["requirements"]["others"]
                    except:
                        point.is_other_required = False

                    point.save()
