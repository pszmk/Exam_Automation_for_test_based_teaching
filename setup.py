from setuptools import setup

setup(name='eaftbt',
	version='1.0',
	# list folders, not files
	packages=['eaftbt',
		'eaftbt.test'],
	scripts=['eaftbt/bin/eaftbt_script.py'],
	package_data={'eaftbt':['data/eaftbt_data.txt']}
	)
