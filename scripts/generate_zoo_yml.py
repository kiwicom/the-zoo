import structlog

from zoo.repos.github import create_remote_commit as create_github_remote_commit
from zoo.repos.github import get_file_content as get_github_file_content
from zoo.repos.gitlab import create_remote_commit as create_gitlab_remote_commit
from zoo.repos.gitlab import get_file_content as get_gitlab_file_content
from zoo.repos.models import Repository
from zoo.repos.zoo_yml import generate, parse, validate
from zoo.services.models import Service

log = structlog.get_logger()


def file_exists(remote_id, path, provider, ref="master"):
    get_file_content = None
    if provider == "github":
        get_file_content = get_github_file_content
    else:
        get_file_content = get_gitlab_file_content

    try:
        _ = get_file_content(remote_id, path, ref)
        return True
    except Exception:
        return False


def generate_file(remote_id, message, actions, branch, provider):
    create_remote_commit = None
    if provider == "gitlab":
        create_remote_commit = create_gitlab_remote_commit

    else:
        create_remote_commit = create_github_remote_commit

    create_remote_commit(remote_id, message, actions, branch)


def main():
    zooyml = ".zoo.yml"

    for service in Service.objects.all():
        remote_id, provider = service.repository.remote_id, service.repository.provider
        if file_exists(remote_id, zooyml, provider):
            continue

        yml = generate(service)

        actions = [{"action": "create", "content": yml, "file_path": zooyml}]
        message = "feat(zoo): add .zoo.yml file"
        branch = "master"

        generate_file(remote_id, message, actions, branch, provider)


if __name__ == "__main__":
    main()
