# Copied by @aexvir from @bence on 2018-09-25

from django.db import migrations


def delete_issues(apps, schema_editor):
    Issue = apps.get_model("auditing", "Issue")
    Issue.objects.filter(kind_key="py_requirements:unhealthy_dependencies").delete()


def reverse_delete_issues(*args):
    print(
        "The database is now missing all py_requirements:unhealthy_dependencies issues. "
        "They will be recreated with the next pull task execution."
    )


class Migration(migrations.Migration):

    dependencies = [("auditing", "0023_remove_dockerfilelint_bear_issue")]

    operations = [migrations.RunPython(delete_issues, reverse_delete_issues)]
