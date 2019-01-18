from zoo.repos import github as uut


class FakeTree:
    def __init__(self, tree_list, base_tree=None):
        self.tree_list = tree_list
        self.base_tree = None

    def __eq__(self, other):
        return self.tree_list == other.tree_list and self.base_tree == other.base_tree


class FakeTreeElem:
    def __init__(self, path, type="blob", mode="100644", **kwargs):
        self._identity = dict(path=path, type=type, mode=mode, **kwargs)

    def __getattr__(self, name):
        return self._identity[name]

    def __eq__(self, other):
        return self._identity == other._identity

    def __repr__(self):
        return f"<FakeTreeElem({self._identity})>"


def test_github_create_remote_commit__create_full_tree(mocker):
    m_commit = mocker.MagicMock(tree=mocker.Mock(sha="bcd"))
    m_new_commit = mocker.MagicMock(sha="def")

    m_project = mocker.Mock(
        get_git_ref=mocker.Mock(
            return_value=mocker.Mock(object=mocker.Mock(sha="abc"))
        ),
        get_git_commit=mocker.Mock(return_value=m_commit),
        get_git_tree=mocker.Mock(
            return_value=mocker.Mock(
                tree=[
                    mocker.Mock(
                        sha="foo.py_sha", path="foo.py", type="blob", mode="100644"
                    ),
                    mocker.Mock(sha="y_sha", path="y", type="tree"),
                    mocker.Mock(
                        sha="y/a.py_sha", path="y/a.py", type="blob", mode="100644"
                    ),
                ]
            )
        ),
        create_git_tree=mocker.Mock(side_effect=FakeTree),
        create_git_commit=mocker.Mock(return_value=m_new_commit),
        create_git_ref=mocker.Mock(),
    )

    m_get_project = mocker.patch("zoo.repos.github.get_project", return_value=m_project)

    mocker.patch("zoo.repos.github._create_tree_element", side_effect=FakeTreeElem)

    actions = [
        {"action": "move", "file_path": "b/foo.py", "previous_path": "foo.py"},
        {"action": "create", "file_path": "test.py", "content": "te\nst"},
        {"action": "delete", "file_path": "y/a.py"},
    ]
    commit_sha = uut.create_remote_commit(123, "test message", actions, "test_branch")
    assert commit_sha == m_new_commit.sha

    m_get_project.assert_called_once_with(123)

    m_project.get_git_ref.assert_called_once_with("heads/master")
    m_project.get_git_commit.assert_called_once_with("abc")
    m_project.get_git_tree.assert_called_once_with("bcd", recursive=True)

    expected_tree_list = [
        FakeTreeElem("b/foo.py", sha="foo.py_sha"),
        FakeTreeElem("test.py", content="te\nst"),
    ]
    m_project.create_git_tree.assert_called_once_with(expected_tree_list)
    m_project.create_git_commit.assert_called_once_with(
        message="test message", parents=[m_commit], tree=FakeTree(expected_tree_list)
    )
    m_project.create_git_ref.assert_called_once_with(
        ref="refs/heads/test_branch", sha=m_new_commit.sha
    )


def test_github_create_remote_commit__update_tree(mocker):
    m_tree = mocker.MagicMock(sha="bcd")
    m_commit = mocker.MagicMock(tree=m_tree)
    m_new_commit = mocker.MagicMock(sha="def")

    m_project = mocker.Mock(
        get_git_ref=mocker.Mock(
            return_value=mocker.Mock(object=mocker.Mock(sha="abc"))
        ),
        get_git_commit=mocker.Mock(return_value=m_commit),
        create_git_tree=mocker.Mock(side_effect=FakeTree),
        create_git_commit=mocker.Mock(return_value=m_new_commit),
        create_git_ref=mocker.Mock(),
    )

    m_get_project = mocker.patch("zoo.repos.github.get_project", return_value=m_project)

    mocker.patch("zoo.repos.github._create_tree_element", side_effect=FakeTreeElem)

    actions = [
        {"action": "update", "file_path": "bar/foo.txt", "content": "content A"},
        {"action": "create", "file_path": "test.py", "content": "content B"},
    ]
    commit_sha = uut.create_remote_commit(123, "test message", actions, "test_branch")
    assert commit_sha == m_new_commit.sha

    m_get_project.assert_called_once_with(123)

    m_project.get_git_ref.assert_called_once_with("heads/master")
    m_project.get_git_commit.assert_called_once_with("abc")

    expected_tree_list = [
        FakeTreeElem("bar/foo.txt", content="content A"),
        FakeTreeElem("test.py", content="content B"),
    ]
    m_project.create_git_tree.assert_called_once_with(
        expected_tree_list, base_tree=m_tree
    )
    m_project.create_git_commit.assert_called_once_with(
        message="test message", parents=[m_commit], tree=FakeTree(expected_tree_list)
    )
    m_project.create_git_ref.assert_called_once_with(
        ref="refs/heads/test_branch", sha=m_new_commit.sha
    )


def test_github_create_merge_request(mocker):
    m_project = mocker.Mock(
        create_pull=mocker.Mock(return_value=mocker.Mock(number=42))
    )
    m_get_project = mocker.patch("zoo.repos.github.get_project", return_value=m_project)

    pull_number = uut.create_merge_request(
        111,
        title="Title Merge Request",
        source_branch="fix_branch",
        description="Description",
    )
    assert pull_number == 42

    m_get_project.assert_called_once_with(111)
    m_project.create_pull.assert_called_once_with(
        title="Title Merge Request",
        head="fix_branch",
        base="master",
        body="Description\n\n---\n\n*via The Zoo*",
    )
