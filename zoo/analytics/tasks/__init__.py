from collections import namedtuple
from functools import partial

from ..models import DependencyType
from .licenses import check_python_lib_licenses
from .snapshots import take_dependency_snapshots

Hit = namedtuple("Hit", ["name", "version", "for_production", "health_status", "type"])
Hit.__new__.__defaults__ = (None, None, None, None)

DockerImage = partial(Hit, type=DependencyType.DOCKER_IMG)
CiTemplate = partial(Hit, type=DependencyType.GITLAB_CI)
JSLibrary = partial(Hit, type=DependencyType.JS_LIB)
Language = partial(Hit, type=DependencyType.LANG)
OS = partial(Hit, type=DependencyType.OS)
PyLibrary = partial(Hit, type=DependencyType.PY_LIB)
