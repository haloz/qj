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

## Reading
* pytest project structure: https://pytest.org/latest/goodpractises.html
* using pytest: https://pytest.org/latest/getting-started.html#our-first-test-run
* article about TDD via pytest: http://lgiordani.com/blog/2015/05/13/python-oop-tdd-example-part1/
* BDD via pytest-bdd: https://pypi.python.org/pypi/pytest-bdd
* setuptools & setup.py: https://pythonhosted.org/setuptools/setuptools.html
* python & integration testing: http://www.fullstackpython.com/integration-testing.html
* article about integration testing: http://enterprisecraftsmanship.com/2015/07/13/integration-testing-or-how-to-sleep-well-at-nights/
