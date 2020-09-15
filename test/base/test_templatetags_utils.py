import pytest
from django import template

from zoo.base.templatetags import utils as uut
from zoo.instance.models import Singleton

STRING_OLD = """import sys
import os

if os.path.exists("test/file"):
    sys.stdout.write("file exists")
"""

STRING_NEW = """import sys
import os

if os.path.exists("test/file"):
    content = os.read(something, os.O_RDWR)
"""

pytestmark = pytest.mark.django_db



def test_templatetags_utils__diff():
    result = uut.diff(STRING_OLD, STRING_NEW)

    assert "".join(result) == (
        "@@ -2,4 +2,4 @@\n"
        " import os\n"
        " \n"
        ' if os.path.exists("test/file"):\n'
        '-    sys.stdout.write("file exists")\n'
        "+    content = os.read(something, os.O_RDWR)\n"
    )


def test_templatestags_utils__singleton__correct():
    provider = uut.singleton("instance.Hints")

    assert provider.pk == Singleton.instance_id


@pytest.mark.parametrize("identifier", ("whatever", "instance.Wrong", "does.not.exist"))
def test_templatestags_utils__singleton__wrong_identifier(identifier):
    with pytest.raises(template.TemplateSyntaxError):
        uut.singleton(identifier)
