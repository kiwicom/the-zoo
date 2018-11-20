# Handwritten by @bence on 2018-09-24

from django.db import migrations


def delete_issues(apps, schema_editor):
    Issue = apps.get_model("auditing", "Issue")
    Issue.objects.filter(kind_key="coafile:use_DockerfileLintBear").delete()


def reverse_delete_issues(*args):
    print(
        "The database is now missing all coafile:use_DockerfileLintBear issues. "
        "They will be recreated with the next pull task execution."
    )


class Migration(migrations.Migration):

    dependencies = [("auditing", "0022_remove_generic_ref_repository")]

    operations = [migrations.RunPython(delete_issues, reverse_delete_issues)]
