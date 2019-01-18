from zoo.base.templatetags import utils as uut


STRING_OLD = """import sys
import os

if os.path.exists("test/file"):
    sys.stdout.write("file exists")
"""

STRING_NEW = """import sys
import os

if os.path.exists("test/file"):
    print("file exists")
"""


def test_templatetags_utils__diff():
    result = uut.diff(STRING_OLD, STRING_NEW)

    assert "".join(result) == (
        "@@ -2,4 +2,4 @@\n"
        " import os\n"
        " \n"
        ' if os.path.exists("test/file"):\n'
        '-    sys.stdout.write("file exists")\n'
        '+    print("file exists")\n'
    )
