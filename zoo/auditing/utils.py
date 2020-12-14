import json
import pathlib
import secrets
import string
import tempfile

import requests

from ..base import redis
from ..repos.utils import download_repository
from . import runner


def create_git_issue(issue, user_name, reverse_url):
    remote_iid = issue.repository.scm_module.create_remote_issue(
        issue, user_name, reverse_url
    )
    issue.remote_issue_id = remote_iid
    issue.full_clean()
    issue.save()


def apply_patches(issue):
    if issue.kind.patch is None:
        return

    with tempfile.TemporaryDirectory() as repo_dir:
        repo_path = download_repository(issue.repository, repo_dir)
        context = runner.CheckContext(issue.repository, repo_path)

        handler = PatchHandler(issue)
        handler.run_patches(context)
        handler.handle_patches()


def generate_random_key(length=512):
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


class ContextObjectSerializer:
    def __init__(self, context):
        self.context = context

    def to_dict(self, obj):
        if isinstance(obj, self.context.CodePatch):
            return self._code_patch_to_dict(obj)
        if isinstance(obj, self.context.RequestPatch):
            return self._request_patch_to_dict(obj)
        return obj._asdict()

    def _code_patch_to_dict(self, patch):
        file_path = pathlib.Path(patch.file_path)
        previous_path = (
            pathlib.Path(patch.previous_path)
            if patch.previous_path is not None
            else None
        )
        repo_path_offset = len(self.context.path.as_posix()) + 1

        data = {
            "action": patch.action,
            "file_path": file_path.as_posix()[repo_path_offset:],
        }

        if patch.action in ["update", "delete"]:
            data["previous_content"] = file_path.read_text()

        if patch.action in ["create", "update"]:
            data["content"] = patch.content

        if previous_path is not None and previous_path != file_path:
            data["previous_path"] = previous_path.as_posix()[repo_path_offset:]

        return data

    def _request_patch_to_dict(self, request_patch):
        patch_data = request_patch._asdict()
        patch_data["action"] = "request"
        return patch_data


class PatchStorage:
    def __init__(self):
        self.redis = redis

    def save(self, patches):
        key = f"_cache.zoo.auditing.PatchStorage.key-{generate_random_key()}"
        redis_conn = self.redis.get_connection()
        redis_conn.set(key, json.dumps(patches), ex=600)
        return key

    def load(self, key):
        redis_conn = self.redis.get_connection()
        value = redis_conn.get(key)
        return json.loads(value)


class PatchHandler:
    def __init__(self, issue, storage=None):
        self.issue = issue

        self._storage = storage or PatchStorage()
        self._patches = []

    def run_patches(self, context):
        self._patches = [
            ContextObjectSerializer(context).to_dict(patch)
            for patch in self.issue.kind.apply_patch(context)
        ]
        return self._patches

    def save_patches(self):
        return self._storage.save(self._patches)

    def load_patches(self, key):
        self._patches = self._storage.load(key)
        return self._patches

    def handle_patches(self, key=None, reverse_url=None):
        if not self._patches and not (key and self.load_patches(key)):
            return False

        requests, actions = [], []

        for patch in self._patches:
            if patch["action"] == "request":
                requests.append(patch)
            else:
                actions.append(patch)

        self._resolve_actions(actions, reverse_url=reverse_url)
        self._resolve_requests(requests)

        return True

    def _resolve_actions(self, actions_data, reverse_url=None):
        if not actions_data:
            return

        branch_name = f"zoo/{self.issue.kind.id}"
        repository = self.issue.repository

        repository.scm_module.create_remote_commit(
            repository.remote_id,
            actions=actions_data,
            message=self.issue.kind.title,
            branch=branch_name,
        )
        self.issue.merge_request_id = repository.scm_module.create_merge_request(
            repository.remote_id,
            title=self.issue.kind.title,
            description=self.issue.description_md,
            source_branch=branch_name,
            reverse_url=reverse_url,
        )
        self.issue.save()

    def _resolve_requests(self, requests_data):
        if not requests_data:
            return

        for data in requests_data:
            req_kwargs = {
                "url": data["url"],
                "method": data["method"],
                "headers": data.get("headers"),
            }
            body = data.get("body")

            if isinstance(body, dict):
                req_kwargs["json"] = body
            else:
                req_kwargs["data"] = body

            resp = requests.request(**req_kwargs)
            resp.raise_for_status()

        self.issue.status = self.issue.Status.FIXED.value
        self.issue.save()
