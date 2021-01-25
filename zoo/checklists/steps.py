import attr
import yaml
from django.conf import settings


@attr.s(frozen=True, slots=True)
class Step:
    tag: str = attr.ib()
    category_name: str = attr.ib(eq=False, order=False, repr=False)
    id: str = attr.ib()
    title: str = attr.ib(eq=False, order=False, repr=False)
    description: str = attr.ib(eq=False, order=False, repr=False, default=None)
    help_url: str = attr.ib(eq=False, order=False, repr=False, default=None)
    is_checked: bool = attr.ib(default=False)

    @property
    def key(self):
        return f"{self.tag}:{self.id}"


class InvalidStepMetadata(Exception):
    pass


class IncorrectStepMetadata(Exception):
    pass


def load_all_steps():
    all_steps = {}

    for steps_file_path in settings.ZOO_CHECKLISTS_ROOT.glob("**/*.yml"):
        try:
            header, items = yaml.safe_load_all(steps_file_path.read_text())
        except (ValueError, KeyError, yaml.scanner.ScannerError) as exc:
            raise InvalidStepMetadata("File format not correct") from exc

        if not items:
            continue

        try:
            all_steps[header["tag"]] = {
                item.key: item
                for item in (Step(**header, **item_details) for item_details in items)
            }
        except TypeError as exc:
            raise IncorrectStepMetadata("Incorrect attributes") from exc

    return all_steps


STEPS = load_all_steps()
