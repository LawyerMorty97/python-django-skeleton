## Python Django Skeleton
#### A skeleton for creating Django APIs in Python :-)

## Dependencies
- django 3.2
- django REST framework
- mypy
- psycopg2 (Postgresql driver)

## Installation
1. Install `pip`
    - Linux: `sudo apt install python3-pip`
    - macOS: `brew install python3` (assuming you're using homebrew)
    - Windows
        - Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) (Right-click to download)
        - Open a new shell window and execute either `python get-pip.py` or `python3 get-pip.py`
2. Install `virtualenv` via PiP
    - Linux/macOS: `sudo pip install virtualenv`
    - Windows: `pip install virtualenv`
3. Configure a new virtual environment
    - Linux/macOS: `virtualenv env`
    - Windows: `python -m virtualenv env`
4. Activate the new virtual environment
    - Not Windows: `source env/activate`
    - Windows: `.\env\Scripts\activate.bat` (Without Git Bash)
      - A: `.\env\Scripts\activate.bat` (Without Git Bash)
      - B: `source .\env\Scripts\activate` (With Git Bash)
5. Install all dependencies with `pip`
    - `pip install -r requirements.txt`
6. Configure Postgres database
    - There are two options
        1. Run an instance of `postgres` with Docker
        2. Have a Postgres database running on your machine
7. Create migrations and migrate to the Postgres database
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
8. Attempt to run the backend
    - `python manage.py runserver`
9. (Optional) Create a Django admin superuser
    - Linux/macOS/Windows?: `python manage.py createsuperuser`
    - Windows: (If using Git Bash) `winpty python manage.py createsuperuser`
    1. Enter a username
    2. Enter an email address
    3. Enter a password
10. (Optional) To deactivate the virtual environment:
    - Linux/macOS: `deactivate`
    - Windows: `.\env\Scripts\deactivate.bat`

# Testing

To run tests:
- `pytest`

To run tests and stop on a failure:
- `pytest -x`

To run a specific test:
- `pytest -k TEST_FUNCTION_NAME_HERE`


# Black [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
We use [black](https://black.readthedocs.io/en/stable/index.html) for formatting code. This means all committed/pushed code should adhere to the black formatting standard. If not, the build will fail, and you will be kindly reminded that you need to format your pushed code.

Black is configured in the `pyproject.toml` file, meaning you can simply run `black .`.

## Avoid ruining `git blame`
To avoid ruining `git blame`, we can instruct git blame to ignore the "black migration commit" by using the `.ignoreRevsFile` option. This way, git blame will work for code committed before we migrated to black. To do so, run the following:
```
git config blame.ignoreRevsFile .git-blame-ignore-revs
```
Here, `.git-blame-ignore-revs` is a file containing the commit identifier for the "black migration commit". Thus, changes in this commit will be ignored when calling `git blame`.

## Run black manually
Usage:
```
black . [--check]
```
If you just want to check the status and don't want to format the files, run black with the `--check` flag.


## IDE Integration
To integrate black, e.g. autoformat on save, in your favorite IDE (PyCharm, VSCode, vim, etc.), follow the [relevant guides](https://black.readthedocs.io/en/stable/integrations/editors.html) from the black docs.