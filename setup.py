from setuptools import setup

setup(
	name='QueryJenkins',
	version="0.1",
	setup_requires=['pytest-runner'],
	tests_require=['pytest', 'pytest-bdd', 'pytest-cov', 'jenkinsapi'],
	install_requires=['jenkinsapi']
)