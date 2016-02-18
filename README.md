# QJ - QueryJenkins
Toolbox for fetching data from Jenkins builds
A python 3 project with virtualenv, pytest, pytest-bdd, pytest-cov

## Setup
* install python3
* pip install virtualenv
* virtualenv qj-env
* qj-env\Scripts\activate
* (pip install setuptools pytest)
* pip install -e .
* (alternative: python setup.py install)

## Run Tests
* python setup.py test
* py.test --cov

## Sublime Text
* SublimeLinter 
* Anaconda
* SublimeOnSaveBuild with python syntax specific config (Python.sublime-settings):
```
{
	"build_on_save" : 1,
	"filename_filter" : "\\.py$"
}
```
* added extra build system to run tests (Python-Run-Tests.sublime-build):
```
{
	"shell_cmd": "py.test --capture=no -s && py.test --cov --capture=no -s",
	"working_dir": "$file_path/.."
}
```

## Reading
* pytest project structure: https://pytest.org/latest/goodpractises.html
* using pytest: https://pytest.org/latest/getting-started.html#our-first-test-run
* article about TDD via pytest: http://lgiordani.com/blog/2015/05/13/python-oop-tdd-example-part1/
* BDD via pytest-bdd: https://pypi.python.org/pypi/pytest-bdd
* setuptools & setup.py: https://pythonhosted.org/setuptools/setuptools.html
* python & integration testing: http://www.fullstackpython.com/integration-testing.html
* article about integration testing: http://enterprisecraftsmanship.com/2015/07/13/integration-testing-or-how-to-sleep-well-at-nights/
* unit testing python / hitchhiker: http://docs.python-guide.org/en/latest/writing/tests/
* sublime config for python: http://piotr.banaszkiewicz.org/blog/2013/08/24/sublime-text-3-for-python-development/