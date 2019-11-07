from zoo.analytics.tasks.utils import DockerImageId


def test_docker_image_id_parsing_short():
    parsed = DockerImageId("python:3.7")
    assert parsed.full_image_id == "python:3.7"
    assert parsed.registry is None
    assert parsed.registry_host_name is None
    assert parsed.registry_port is None
    assert parsed.full_image_name == "python:3.7"
    assert parsed.full_image_name_no_tag == "python"
    assert parsed.username is None
    assert parsed.full_repository_name == "python"
    assert parsed.repository_name == "python"
    assert parsed.namespaces is None
    assert parsed.tag == "3.7"
    assert parsed.version == "3.7"
    assert parsed.full_os is None
    assert parsed.os is None
    assert parsed.os_version is None
    assert parsed.alias is None


def test_docker_image_id_parsing_short_with_os():
    parsed = DockerImageId("python:3.7-alpine")
    assert parsed.full_image_id == "python:3.7-alpine"
    assert parsed.registry is None
    assert parsed.registry_host_name is None
    assert parsed.registry_port is None
    assert parsed.full_image_name == "python:3.7-alpine"
    assert parsed.full_image_name_no_tag == "python"
    assert parsed.username is None
    assert parsed.full_repository_name == "python"
    assert parsed.repository_name == "python"
    assert parsed.namespaces is None
    assert parsed.tag == "3.7-alpine"
    assert parsed.version == "3.7"
    assert parsed.full_os == "alpine"
    assert parsed.os == "alpine"
    assert parsed.os_version is None
    assert parsed.alias is None


def test_docker_image_id_parsing_short_with_os_version():
    parsed = DockerImageId("python:3.7-alpine3.9")
    assert parsed.full_image_id == "python:3.7-alpine3.9"
    assert parsed.registry is None
    assert parsed.registry_host_name is None
    assert parsed.registry_port is None
    assert parsed.full_image_name == "python:3.7-alpine3.9"
    assert parsed.full_image_name_no_tag == "python"
    assert parsed.username is None
    assert parsed.full_repository_name == "python"
    assert parsed.repository_name == "python"
    assert parsed.namespaces is None
    assert parsed.tag == "3.7-alpine3.9"
    assert parsed.version == "3.7"
    assert parsed.full_os == "alpine3.9"
    assert parsed.os == "alpine"
    assert parsed.os_version == "3.9"
    assert parsed.alias is None


def test_docker_image_id_parsing_localhost():
    parsed = DockerImageId("localhost:5005/bi/airflow/celery as base")
    assert parsed.full_image_id == "localhost:5005/bi/airflow/celery as base"
    assert parsed.registry == "localhost:5005"
    assert parsed.registry_host_name == "localhost"
    assert parsed.registry_port == "5005"
    assert parsed.full_image_name == "bi/airflow/celery as base"
    assert parsed.full_image_name_no_tag == "bi/airflow/celery"
    assert parsed.username == "bi"
    assert parsed.full_repository_name == "airflow/celery"
    assert parsed.repository_name == "airflow"
    assert parsed.namespaces == ["celery"]
    assert parsed.tag is None
    assert parsed.version is None
    assert parsed.full_os is None
    assert parsed.os is None
    assert parsed.os_version is None
    assert parsed.alias == "base"


def test_docker_image_id_parsing_localhost_no_port():
    parsed = DockerImageId("localhost/airflow/celery:1.0")
    assert parsed.full_image_id == "localhost/airflow/celery:1.0"
    assert parsed.registry == "localhost"
    assert parsed.registry_host_name == "localhost"
    assert parsed.registry_port is None
    assert parsed.full_image_name == "airflow/celery:1.0"
    assert parsed.full_image_name_no_tag == "airflow/celery"
    assert parsed.username == "airflow"
    assert parsed.full_repository_name == "celery"
    assert parsed.repository_name == "celery"
    assert parsed.namespaces is None
    assert parsed.tag == "1.0"
    assert parsed.version == "1.0"
    assert parsed.full_os is None
    assert parsed.os is None
    assert parsed.os_version is None
    assert parsed.alias is None


def test_docker_image_id_parsing_long():
    parsed = DockerImageId(
        "registry.com:5005/group/my-image/name1/name2:0.1.1-alpine3.9 as   base-image"
    )
    assert (
        parsed.full_image_id
        == "registry.com:5005/group/my-image/name1/name2:0.1.1-alpine3.9 as base-image"
    )
    assert parsed.registry == "registry.com:5005"
    assert parsed.registry_host_name == "registry.com"
    assert parsed.registry_port == "5005"
    assert (
        parsed.full_image_name
        == "group/my-image/name1/name2:0.1.1-alpine3.9 as base-image"
    )
    assert parsed.full_image_name_no_tag == "group/my-image/name1/name2"
    assert parsed.username == "group"
    assert parsed.full_repository_name == "my-image/name1/name2"
    assert parsed.repository_name == "my-image"
    assert parsed.namespaces == ["name1", "name2"]
    assert parsed.tag == "0.1.1-alpine3.9"
    assert parsed.version == "0.1.1"
    assert parsed.full_os == "alpine3.9"
    assert parsed.os == "alpine"
    assert parsed.os_version == "3.9"
    assert parsed.alias == "base-image"
