import re
from collections import Counter

import structlog

from zoo.repos.models import Repository
from zoo.services.models import Service

log = structlog.get_logger()


def normalize(text: str) -> str:
    return re.sub(r"\W", "", text).lower()


def score_repos(service, repos):
    """Return how likely each repo being a match is.

    +10 score for:
        repo name in service name 10
        service name in repo name 10
    +1 score for:
        repo owner in service owner 0
        service owner in repo owner 1
    """
    scores = Counter()
    for repo in repos:
        if normalize(service.name) in normalize(repo.name):
            scores[repo] += 10
        if normalize(repo.name) in normalize(service.name):
            scores[repo] += 10
        if normalize(service.owner) in normalize(repo.owner):
            scores[repo] += 1
        if normalize(repo.owner) in normalize(service.owner):
            scores[repo] += 1
    return scores


def main():
    repos = Repository.objects.all()
    log.info(f"Got {len(repos)} repos")
    for service in Service.objects.all():
        if service.repository:
            log.info(f"Skipping {service} (has repo already)")
            continue
        log.info(f"Running for {service}")
        scores = score_repos(service, repos)
        likely_repos = scores.most_common(2)
        if not likely_repos:
            log.info(f"No repos matching at all")
            continue
        if len(likely_repos) == 2 and likely_repos[0][1] == likely_repos[1][1]:
            log.info(f"No certain match between {likely_repos}")
            continue
        service.repository = likely_repos[0][0]
        log.info(f"Linked {service} to {service.repository}")
        service.save()


if __name__ == "__main__":
    main()
