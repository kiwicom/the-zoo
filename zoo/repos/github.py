from django.conf import settings
from github import Github, GithubException
from github.GithubException import UnknownObjectException
from github.GithubObject import NotSet
import requests
from retry import retry

from .exceptions import MissingFilesError, RepositoryNotFoundError

github = Github(settings.GITHUB_TOKEN)

github_retry = retry(
    (requests.RequestException, GithubException), tries=5, delay=2, backoff=2
)


@github_retry
def get_repositories():
    for repo in github.get_user().get_repos():
        yield {
            "id": repo.id,
            "provider": "github",
            "owner": repo.owner.login,
            "name": repo.name,
            "url": repo.svn_url,
        }


@github_retry
def get_project(github_id):
    try:
        project = github.get_repo(github_id)
    except UnknownObjectException:
        raise RepositoryNotFoundError
    return project


@github_retry
def download_archive(project, archive, sha=None):
    archive.seek(0)  # needed if retry
    sha = sha if sha else NotSet
    archive_url = project.get_archive_link("tarball", ref=sha)
    r = requests.get(archive_url, stream=True)
    if r.status_code == requests.codes.not_found:
        raise MissingFilesError
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            archive.write(chunk)
    return archive


@github_retry
def get_project_details(github_id):
    project = get_project(github_id)
    return {
        "id": project.id,
        "name": project.full_name,
        "description": project.description,
        "avatar": None,
        "url": project.svn_url,
        "readme": project.get_readme().url,
        "stars": project.stargazers_count,
        "forks": project.forks_count,
        "branch_count": project.get_branches().totalCount,
        "member_count": project.get_contributors().totalCount,
        "issue_count": project.get_issues().totalCount,
        "last_activity_at": project.updated_at,
    }


@github_retry
def get_languages(remote_id):
    langs = get_project(remote_id).get_languages()
    sum_of_bytes = sum(langs.values())
    langs_percent = {}
    for lang, num in langs.items():
        langs_percent[lang] = round(num / sum_of_bytes * 100, 2)
    return langs_percent


@github_retry
def create_remote_issue(issue, user_name, reverse_url):
    github_issue = issue.repository.remote_git_object.create_issue(
        title=f"{issue.kind.category}: {issue.kind.title}",
        body=issue.description_md
        + (
            "\n\n---\n\n"
            f"severity: {issue.kind.severity.value} ; effort: {issue.kind.effort.value} "
            f"*This issue was created by @{user_name} "
            f"via [The Zoo]({reverse_url})*"
        ),
    )

    return github_issue.number
