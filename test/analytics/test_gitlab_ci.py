import yaml

from zoo.analytics.tasks import gitlab_ci as uut

YAML = """\
stages:
  - build
  - test
  - release
  - deploy

image: docker:19.03

include:
  - 'https://ci-files.skypicker.com/templates/build/coala.yml'
  - 'https://ci-files.skypicker.com/templates/build/black.yml'
  - 'https://ci-files.skypicker.com/templates/build/docker_build.yml'
  - 'https://ci-files.skypicker.com/templates/release/sonarqube_scan.yml'
  - 'https://ci-files.skypicker.com/templates/deploy/.crane.yml'
  - template: 'Workflows/Branch.yml'
  - local: '/templates/localfile.yml'
  - project: 'grp/prj'
    ref: v1.0.0
    file: '/templates/.builds.yml'
  - project: 'grp/prj'
    file:
      - '/templates/.builds.yml'
      - '/templates/.tests.yml'
  - remote: 'https://gitlab.com/example-project/-/raw/master/.gitlab-ci.yml'

black:
  stage: lint-and-build
  image: kiwicom/black:19.3b0
  script:
    - black -l 120 --check --fast docs kw scripts test run.py setup.py

deploy_production:
  extends: .crane
  variables:
    CRANE_SLACK_CHANNEL: the-zoo
  environment:
    name: production
    url: https://zoo.skypicker.com
  when: manual

kubeval:
  stage: test
  image:
    name: kiwicom/kubeval
    entrypoint: kubeval
  script:
    - analyze k8s
"""


def test_parse_docker_images():
    expected_images = [
        ("docker", "19.03"),
        ("kiwicom/black", "19.3b0"),
        ("kiwicom/kubeval", "latest"),
    ]
    parsed_yaml = yaml.safe_load(YAML)

    images = uut.parse_docker_images(parsed_yaml)

    assert len(list(images)) == 3

    for image in images:
        assert image.name, image.version in expected_images


def test_parse_gitlab_ci_template():
    expected_templates = [
        "coala",
        "black",
        "docker_build",
        "sonarqube_scan",
        ".crane",
        "template:Workflows/Branch.yml",
        "local:/templates/localfile.yml",
        "repo:grp/prg//templates/.builds.yml@v1.0.0",
        "repo:grp/prg//templates/.builds.yml",
        "repo:grp/prg//templates/.tests.yml",
        "remote:https://gitlab.com/example-project/-/raw/master/.gitlab-ci.yml",
    ]
    parsed_yaml = yaml.safe_load(YAML)

    templates = uut.parse_gitlab_ci_template(parsed_yaml)

    assert len(list(templates)) == 11

    for template in templates:
        assert template.name in expected_templates
