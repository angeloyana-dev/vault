from setuptools import setup, find_packages

setup(
	name='vault',
	version='1.0.0',
	description='A simple cli tool for managing sensitive data like passwords and apikeys.',
	author='Angelo Yana',
	author_email='angeloyana.dev@gmail.com',
	url='https://github.com/angeloyana-dev/vault',
	license='MIT',
	packages=find_packages(),
	install_requires=['termcolor', 'cryptography'],
	entry_points={
		'console_scripts': [
			'vault = vault.main:main'
		]
	},
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3'
	]
)