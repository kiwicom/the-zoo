import base64

from graphene.relay import PageInfo

DEFAULT_PAGE_LENGHT = 10


class MissingBeforeValueError(Exception):
    pass


def encode_cursor(num):
    return base64.b64encode(str(num).encode("utf-8")).decode("utf-8")


def decode_cursor(cursor):
    return int(base64.b64decode(cursor).decode("utf-8"))


class Paginator:
    def __init__(
        self,
        *,
        first=None,
        after=None,
        last=None,
        before=None,
        per_page=DEFAULT_PAGE_LENGHT,
        **kwargs
    ):
        self.per_page = per_page

        slice_from = 0
        slice_to = per_page

        if first is not None:
            if after is not None:
                slice_from = decode_cursor(after)
            slice_to = slice_from + first

        elif last is not None:
            if before is None:
                raise MissingBeforeValueError(
                    'Pagination "last" works only in combination with "before" argument.'
                )

            slice_to = decode_cursor(before) - 1
            slice_from = slice_to - last
            if slice_from < 0:
                slice_from = 0

        self.slice_from = slice_from
        self.slice_to = slice_to

    def get_page_info(self, total):
        has_previous_page = False
        has_next_page = False
        start_cursor = None
        end_cursor = None

        if self.slice_from < self.slice_to and self.slice_from < total:
            start_cursor = encode_cursor(self.slice_from + 1)

            if self.slice_to > total:
                end_cursor = encode_cursor(total)
            else:
                end_cursor = encode_cursor(self.slice_to)

            if self.slice_from > 0:
                has_previous_page = True

            if self.slice_to < total:
                has_next_page = True

        return PageInfo(
            has_previous_page=has_previous_page,
            has_next_page=has_next_page,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
        )

    def get_edge_cursor(self, num):
        return encode_cursor(self.slice_from + num)
