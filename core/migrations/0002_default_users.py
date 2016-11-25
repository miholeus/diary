# coding: utf-8

from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'users.json')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(loadfixture)
    ]

    def unapply(self, project_state, schema_editor, collect_sql=False):
        migrations.RunSQL("TRUNCATE TABLE users")
