import pytest

from zoo.api.paginator import (
    DEFAULT_PAGE_LENGHT,
    encode_cursor,
    decode_cursor,
    Paginator,
    MissingBeforeValueError,
)


@pytest.mark.parametrize("num, cursor", [(5, "NQ=="), (777, "Nzc3"), (12, "MTI=")])
def test_encode_cursor(num, cursor):
    assert encode_cursor(num) == cursor


@pytest.mark.parametrize("num, cursor", [(8, "OA=="), (123, "MTIz"), (65, "NjU=")])
def test_decode_cursor(num, cursor):
    assert decode_cursor(cursor) == num


def test_encode_and_decode_cursor():
    assert decode_cursor(encode_cursor(42)) == 42


def test_paginator__defaults():
    paginator = Paginator()
    assert paginator.slice_from == 0
    assert paginator.slice_to == DEFAULT_PAGE_LENGHT


def test_paginator__custom_per_page():
    paginator = Paginator(per_page=5)
    assert paginator.per_page == 5
    assert paginator.slice_from == 0
    assert paginator.slice_to == 5


@pytest.mark.parametrize(
    "kw, slice_from, slice_to",
    [
        ({"first": 15}, 0, 15),
        ({"first": 5, "after": encode_cursor(3)}, 3, 8),
        ({"last": 8, "before": encode_cursor(20)}, 11, 19),
        # overflow of slice_from
        ({"last": 100, "before": encode_cursor(42)}, 0, 41),
        # preffer first before last if both provided
        ({"first": 20, "last": 4}, 0, 20),
    ],
)
def test_paginator__input_combinations(kw, slice_from, slice_to):
    paginator = Paginator(**kw)
    assert paginator.slice_from == slice_from
    assert paginator.slice_to == slice_to


def test_paginator__last_without_before():
    with pytest.raises(MissingBeforeValueError):
        Paginator(last=1)


@pytest.mark.parametrize(
    "kw, total, previous, next, start, end",
    [
        ({}, 10, False, False, 1, 10),
        ({}, 15, False, True, 1, 10),
        ({}, 5, False, False, 1, 5),
        ({"first": 1}, 10, False, True, 1, 1),
        ({"first": 6}, 10, False, True, 1, 6),
        ({"first": 6}, 4, False, False, 1, 4),
        ({"first": 6}, 6, False, False, 1, 6),
        ({"first": 3, "after": encode_cursor(7)}, 20, True, True, 8, 10),
        ({"first": 3, "after": encode_cursor(17)}, 20, True, False, 18, 20),
        ({"first": 5, "after": encode_cursor(17)}, 20, True, False, 18, 20),
        ({"last": 4, "before": encode_cursor(10)}, 20, True, True, 6, 9),
        ({"last": 4, "before": encode_cursor(5)}, 20, False, True, 1, 4),
        ({"last": 4, "before": encode_cursor(3)}, 20, False, True, 1, 2),
        # out of bounds
        ({"first": 3, "after": encode_cursor(10)}, 10, False, False, None, None),
        ({"last": 3, "before": encode_cursor(1)}, 10, False, False, None, None),
    ],
)
def test_paginator__get_page_info(kw, total, previous, next, start, end):
    paginator = Paginator(**kw)
    page_info = paginator.get_page_info(total)
    assert page_info.has_previous_page is previous
    assert page_info.has_next_page is next
    assert page_info.start_cursor == start if start is None else encode_cursor(start)
    assert page_info.end_cursor == end if end is None else encode_cursor(end)


@pytest.mark.parametrize(
    "kw, num, cursor",
    [
        ({}, 3, encode_cursor(3)),
        ({"first": 6, "after": encode_cursor(1)}, 3, encode_cursor(4)),
        ({"last": 6, "before": encode_cursor(11)}, 3, encode_cursor(7)),
    ],
)
def test_paginator__get_edge_cursor(kw, num, cursor):
    paginator = Paginator(**kw)
    assert paginator.get_edge_cursor(num) == cursor
