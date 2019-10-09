The Zoo
=======

A smart service catalogue providing an overview of your services' development and operations.

Adding custom checks
====================

If you want to add your own checks to the zoo, you will need to create your own project with a python package in the directory specified by the :code:`ZOO_AUDITING_ROOT` environment variable. By default, the variable is pointing to :code:`zoo/auditing/standards`. (Don't forget that as for any other python package all folders need to have a :code:`__init__.py` file.) You can also install the package to this directory if your package is uploaded to PyPI.

The package needs to have two directories:

- metadata folder with :code:`yml` files holding the list of errors code can trigger
- checks folder with python :code:`check_` functions that actually perform the checks

Both of them need to be *importable by the zoo* and the metadata and checks filenames have to match (the zoo imports the metadata files based on the python check filename).

**Structure example:**
-----------------

.. code-block:: shell
    zoo
    └── auditing
        └── standards
            └── zoo_kiwicom_standards
                ├── __init__.py
                ├── checks
                │   ├── __init__.py
                │   ├── check_requirements_py.py
                │   └── check_security.py
                └── metadata
                    ├── __init__.py
                    ├── check_requirements_py.yml
                    └── check_security.yml

Metadata
--------

Metadata is stored in yaml files with a list of errors your checks yield and their details. There are two compulsory parameters in the header:

- :code:`namespace`
- :code:`category`

Then you describe the errors with the following parameters:

- :code:`id` - a unique identifier (*required*)
- :code:`title` - a human-readable title (*required*)
- :code:`description` - additional information about the error (*optional*)
  - :code:`{details}` - object you can fill with information when yielding the error. Then you pass the :code:`{details}` object to the description where it is rendered (*optional*)

**Real life example:**

.. code-block:: yaml

    namespace: py_security
    category: Security Issues in Python Code
    ---
    - id: user_input_improperly_handled
      severity: critical
      effort: medium
      title: Handle user input correctly
      description: |
        Applications with improperly handled user input become vulnerable to attacks like
        command injection, SSRF, SQL injection, XSS, directory traversal etc.

        [PyT](https://github.com/python-security/pyt) reported security vulnerabilities
        in the following files:

        {details}

Checks
------

The Zoo scanns for all files that have the prefix :code:`check_`, inside those files, it also scans for all functions that have the prefix :code:`check_` (if you need any helper function just name it anything else).

All :code:`check_` functions need to have an input parameter :code:`context`.

:code:`context` is an object of the CheckContext class (`definition <https://github.com/kiwicom/the-zoo/blob/master/zoo/auditing/runner.py#L15>`_), the object will provide information about the code that is checked so the checks can be more selective about how they run.

The Zoo gets an archive of the repository and it extracts it in a temporary directory. None of the changes made to the source code files will be persisted in any way. The most useful parameter of the CheckContext object is :code:`path`, which exposes the temporary path where the source code is extracted.

All :code:`check_` functions should return an iterable. The recommended way is to yield a result as soon as you discover the errors.

The iterable elements should be instances of the :code:`context.Result` (`definition <https://github.com/kiwicom/the-zoo/blob/master/zoo/auditing/runner.py#L10>`_) :code:`namedtuple`, whose fields are the following:

- :code:`namespace` is the namespace from your metadata file
- :code:`id` is the id of the raised error from your metadata file
- :code:`True/False` determines if the error was found (true if it was, false if it was not).
- :code:`details` is an object you can fill with information when yielding the error. Then you pass the :code:`{details}` object to the description where it is rendered (*optional*).

**Check function structure:**

.. literalinclude:: ..\zoo\auditing\standards\dummy_standards\checks\check_constantly.py
    :language: python

**Real life example:**

.. code-block:: python

    def check_dockerignore(context):
        if not (context.path / "Dockerfile").is_file():
            return

        try:
            dockerignore_text = (context.path / ".dockerignore").read_text()
        except FileNotFoundError:
            dockerignore_text = ""  # no dockerignore is effectively an empty dockerignore

        yield context.Result("dockerignore:create_dockerignore", not dockerignore_text)
        yield context.Result("dockerignore:ignore_dotgit", ".git" not in dockerignore_text)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
