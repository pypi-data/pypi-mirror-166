import os, sys
import setuptools

if __name__ == '__main__':

	with open("README.rst", 'r') as long_file:
		long_descript = long_file.read()
	setuptools.setup(
		name='myusefulmetaclasses',
		version='0.0.5',
		install_requires=["wheel"],
		packages=setuptools.find_packages(exclude=['tests']),
		tests_require=['pytest'],
		author='Emiliano Minerba',
		author_email='emi.nerba@gmail.com',
		description="This is MUM: My Useful Metaclasses",
		long_description=long_descript,
		long_description_content_type='text/x-rst',
		license='GPL',
		url='https://gitlab.com/kikulacho92/cruscoplanets',
	)
