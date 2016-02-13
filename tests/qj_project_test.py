from app import qj
from pytest_bdd import scenario, given, when, then

@scenario('qj_project.feature', 'Pass a test')
def test_qj():
	pass

@given('A test method is valid')
def test_validvalue():
	assert qj.gettestvalue() == 'true'

@given('A second method returns a 0')
def test_methodreturnszero():
	assert qj.zeromethod() == 0

@then('The output should be "ok"')
def test_output_value_ok():
	assert qj.getokvalue() == "ok"