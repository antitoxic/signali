import csv
from django.db import transaction
from django.core.management.base import BaseCommand
from signali_location.models import Area, AreaSize


def clean(value, capitalize=False):
    value = value.strip()
    if value == '':
        return None
    return value if not capitalize else value[0].upper() + value[1:]


class Command(BaseCommand):
    help = 'Run to import data from government GIS database exports'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str, choices=['obshtina', 'oblast', 'grad'])
        parser.add_argument('dump', type=str)

    def handle(self, *args, **options):
        delimiter = ',' if options['type'] == 'grad' else ';'
        reader = csv.DictReader(open(options["dump"], newline=''), delimiter=delimiter)

        with transaction.atomic(), Area.objects.disable_mptt_updates():
            type_to_title_mapping = {
                'oblast': "Област",
                'obshtina': "Община",
                'grad': "Град",
            }
            size = AreaSize.objects.get(title=type_to_title_mapping[options['type']])
            obshtina_size = AreaSize.objects.get(title=type_to_title_mapping['obshtina'])
            root_node = Area.objects.get(title__startswith='Навсякъде')
            obshtina_cache = {}
            new_grad_list = []

            for row in reader:
                title = clean(row['name'], True)
                try:
                    area = Area.objects.get(title=title, size=size)
                    if area.regulation_code:
                        raise ValueError("Area with the same name already imported")
                    is_new = False
                except:
                    area = Area(is_public=True, title=title, size=size, parent=root_node)
                    is_new = True

                area.regulation_code = clean(row["ekatte"])

                if options['type'] == 'obshtina':
                    area.regulation_codename = clean(row["obstina"])
                    area.save()

                if options['type'] == 'oblast':
                    area.regulation_codename = clean(row["oblast"])
                    area.save()
                    children = Area.objects.filter(
                        size=obshtina_size,
                        regulation_codename__startswith=area.regulation_codename
                    )
                    children.update(parent=area)

                if options['type'] == 'grad':
                    print("Processing:", title, '...')
                    area.regulation_type = clean(row["t_v_m"])
                    obshtina = clean(row['obstina'])
                    if obshtina not in obshtina_cache:
                        obshtina_cache[obshtina] = Area.objects.get(size=obshtina_size, regulation_codename=obshtina)
                    obshtina = obshtina_cache[obshtina]
                    area.parent = obshtina
                    # performance
                    if is_new:
                        area.tree_id = obshtina.tree_id
                        area.level = obshtina.level + 1
                        area.lft = 1
                        area.rght = 1
                        new_grad_list.append(area)
                    else:
                        area.save()

            if options['type'] == 'grad':
                Area.objects.bulk_create(new_grad_list)

            print('Rebuilding tree...')
            Area.objects.rebuild()
