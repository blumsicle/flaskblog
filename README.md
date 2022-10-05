# Smoothblog

This is a simple blog website. It allows users to register for an account, login, and logout. Once logged
in they can create blog posts that will be displayed on the home page. Users can delete their own blogs.
As well, there is an admin user that can view all users and delete any blog or user.

It is built using Flask as well as some extensions within the Flask ecosystem:

- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)

## Usage

To setup and run this app, first create a virtualenv, then install it within the activated virtualenv. This
will also install the dependencies needed to run:

```sh
virutalenv env
. venv/bin/activate
pip install -e .
```

You will also need to create a `.env` file to hold your configuration variables. You can simply move the
provided `.env.sample` to `.env` and modify the variables as needed.

Once setup you can first run `flask init-db` to initialize the database, then run `flask run` to start the
server. By default it will run on [http://localhost:5000](http://localhost:5000), but that can be changed
with the `--host` and `--port` options. See `flask run --help` for more information.

```shell_session
$ flask init-db
$ flask run
 * Serving Flask app 'smoothblog'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production
WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 430-061-220
```

## Testing

This app uses [pylint](https://pylint.pycqa.org/en/latest/), [pytest](https://docs.pytest.org/en/7.1.x/),
and [coverage](https://coverage.readthedocs.io/en/6.4.4/) to ensure the code is correct and that the tests
are covering **100%** of the code. To test this project, first ensure you have activated the virtualenv,
then install the dependencies:

```sh
. venv/bin/activate
pip install -e '.[dev]'
```

Once the dependencies are installed, you can run `pylint smoothblog` to analyze the code and `pytest --cov`
to run the tests and print out a coverage report.

```shell_session
$ pylint smoothblog

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

$ pytest --cov
=========================================== test session starts ===========================================
platform linux -- Python 3.10.7, pytest-7.1.3, pluggy-1.0.0
rootdir: /home/blum/src/smoothstack/assignments/week02_eval, configfile: pyproject.toml
plugins: cov-3.0.0
collected 41 items

tests/test_auth.py ..........................                                                       [ 63%]
tests/test_blog.py ...........                                                                      [ 90%]
tests/test_models.py ..                                                                             [ 95%]
tests/test_other.py ..                                                                              [100%]

---------- coverage: platform linux, python 3.10.7-final-0 -----------
Name                          Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------
smoothblog/__init__.py           20      0      2      0   100%
smoothblog/auth.py               76      0     20      0   100%
smoothblog/blog.py               41      0      6      0   100%
smoothblog/cli.py                17      0      0      0   100%
smoothblog/database.py            2      0      0      0   100%
smoothblog/forms.py              15      0      6      0   100%
smoothblog/login_manager.py      16      0      2      0   100%
smoothblog/models.py             31      0      4      0   100%
---------------------------------------------------------------
TOTAL                           218      0     40      0   100%


=========================================== 41 passed in 6.48s ============================================
```
