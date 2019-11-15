import json

import fakeredis
import httpretty
import pytest

from zoo.auditing import utils as uut

pytestmark = pytest.mark.django_db


class StorageMock:
    def __init__(self, storage_key):
        self.data = {}
        self.storage_key = storage_key

    def load(self, key):
        return self.data.get(key)

    def save(self, patches):
        self.data[self.storage_key] = patches
        return self.storage_key


def patch_example(context):
    path_str = context.path.resolve().as_posix()
    yield context.CodePatch("create", content="test", file_path=f"{path_str}/test.py")
    yield context.RequestPatch("https://kiwi.com", method="POST", body={"a": "b"})


def test_generate_random_key():
    keys = {uut.generate_random_key(length=32) for _ in range(10)}

    assert isinstance(next(iter(keys)), str)
    assert len(next(iter(keys))) == 32
    assert len(keys) == 10


def test_context_object_serializer(repository, check_context):
    serializer = uut.ContextObjectSerializer(check_context)

    result = check_context.Result("test:key", False)
    assert serializer.to_dict(result) == {
        "issue_key": "test:key",
        "is_found": False,
        "details": None,
    }

    path_str = check_context.path.resolve().as_posix()

    patch1 = check_context.CodePatch(
        action="create", file_path=f"{path_str}/test.py", content="numbers = range(5)"
    )
    assert serializer.to_dict(patch1) == {
        "action": "create",
        "file_path": "test.py",
        "content": "numbers = range(5)",
    }

    patch2 = check_context.CodePatch(
        action="move", file_path=f"{path_str}/a.py", previous_path=f"{path_str}/b.py"
    )
    assert serializer.to_dict(patch2) == {
        "action": "move",
        "file_path": "a.py",
        "previous_path": "b.py",
    }

    request_patch = check_context.RequestPatch(
        "https://www.example.com",
        method="GET",
        body={"this": "that"},
        headers={"Authorization": "Bearer 123"},
    )
    assert serializer.to_dict(request_patch) == {
        "action": "request",
        "method": "GET",
        "url": "https://www.example.com",
        "body": {"this": "that"},
        "headers": {"Authorization": "Bearer 123"},
    }


def test_patch_storage(mocker):
    storage = uut.PatchStorage()

    key = "a1b2c3"
    patches_key = f"_cache.zoo.auditing.PatchStorage.key-{key}"
    patches = [{"this": "that"}]

    redis = fakeredis.FakeStrictRedis()

    mocker.patch("zoo.auditing.utils.generate_random_key", return_value=key)
    mocker.patch("zoo.base.redis.get_connection", return_value=redis)

    storage.save(patches)
    assert json.loads(redis.get(patches_key)) == patches

    result = storage.load(patches_key)
    assert result == patches


@httpretty.activate
def test_patch_handler(mocker, issue_factory, kind_factory, check_context):
    kind = kind_factory(patch="patch_example")
    issue = issue_factory(kind_key=kind.key)

    mocker.patch("zoo.auditing.check_discovery.PATCHES", {kind.key: patch_example})
    mocker.patch("zoo.auditing.models.KINDS", {kind.key: kind})

    m_create_remote_commit = mocker.Mock()
    m_create_merge_request = mocker.Mock(return_value=1)

    mocker.patch(
        "zoo.repos.models.get_scm_module",
        mocker.Mock(
            return_value=mocker.Mock(
                create_remote_commit=m_create_remote_commit,
                create_merge_request=m_create_merge_request,
            )
        ),
    )

    key = "abc"
    storage = StorageMock(key)

    handler = uut.PatchHandler(issue, storage=storage)

    patches = handler.run_patches(check_context)
    assert len(patches) == 2

    handler.save_patches()
    assert len(storage.data[key]) == 2

    handler2 = uut.PatchHandler(issue, storage=storage)
    assert handler2.handle_patches(key=f"not_{key}") is False

    httpretty.register_uri(
        httpretty.POST, "https://kiwi.com", body=json.dumps({"success": True})
    )

    handled = handler2.handle_patches(key=key)

    assert handled is True
    assert httpretty.last_request().body == b'{"a": "b"}'

    m_create_remote_commit.assert_called_once()
    m_create_merge_request.assert_called_once()

    assert issue.merge_request_id == 1
