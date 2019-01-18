from zoo.repos import gitlab as uut


def test_gitlab_create_remote_commit(mocker):
    m_commits_create = mocker.Mock(
        return_value=mocker.Mock(get_id=mocker.Mock(return_value=345))
    )
    m_project = mocker.Mock(commits=mocker.Mock(create=m_commits_create))
    m_get_project = mocker.patch("zoo.repos.gitlab.get_project", return_value=m_project)

    actions = [{"action": "move", "file_path": "a", "previous_path": "b"}]
    commit_id = uut.create_remote_commit(
        222, message="Title Merge Request", actions=actions, branch="fix_that_issue"
    )
    assert commit_id == 345

    m_get_project.assert_called_once_with(222)
    m_commits_create.assert_called_once_with(
        {
            "commit_message": "Title Merge Request",
            "actions": actions,
            "branch": "fix_that_issue",
            "start_branch": "master",
        }
    )


def test_gitlab_create_merge_request(mocker):
    m_create_mr = mocker.Mock(
        return_value=mocker.Mock(get_id=mocker.Mock(return_value=234))
    )
    m_project = mocker.Mock(mergerequests=mocker.Mock(create=m_create_mr))
    m_get_project = mocker.patch("zoo.repos.gitlab.get_project", return_value=m_project)

    merge_request_id = uut.create_merge_request(
        111,
        title="Title Merge Request",
        source_branch="fix_branch",
        description="Description",
    )
    assert merge_request_id == 234

    m_get_project.assert_called_once_with(111)
    m_create_mr.assert_called_once_with(
        {
            "title": "Title Merge Request",
            "source_branch": "fix_branch",
            "target_branch": "master",
            "description": "Description\n\n---\n\n*via The Zoo*",
        }
    )
