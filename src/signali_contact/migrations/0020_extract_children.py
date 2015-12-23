# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from copy import copy

from django.db import models, migrations

def extract_branches(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Organisation = apps.get_model("signali_contact", "Organisation")
    for org in Organisation.objects.all():
        children_groups = {}
        for point in org.contact_points.all():
            short = point.title[:10]
            children_groups[short] = org.contact_points.filter(title__startswith=short)

        for key, points in children_groups.items():
            if len(points) == 0:
                continue
            parent = points[0].clone()
            for child in points:
                child.parent = parent
                child.title = ''
                if child.email:
                    child.source_url = child.url
                    child.url = None
                child.save(update_parent=False)

            parent.precalculate_feedback_stats()
            parent.aggregate_children_visibility()
            parent.save()


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0019_auto_20151223_1039'),
        ('signali_location', '0004_auto_20151209_1200'),
    ]

    operations = [
        migrations.RunPython(extract_branches),
    ]
