from setuptools import setup,find_packages
import os
import shutil

#remove the dist folder first if exists
if os.path.exists("dist"):
	shutil.rmtree("dist")

def readme():
	with open('README.rst') as f:
		return(f.read())

VERSION = '1.0.0'

def write_version_py(filename='SigProfilerTopographyCombiner/version.py'):
	# Copied from numpy setup.py
	cnt = """
# THIS FILE IS GENERATED FROM SIGPROFILERTOPOGRAPHYCOMBINER SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
	
	"""
	fh = open(filename, 'w')
	fh.write(cnt % {'version': VERSION,})
	fh.close()

write_version_py()

setup(name="SigProfilerTopographyCombiner",
    version=VERSION,
    author="Burcak Otlu",
    author_email="burcakotlu@eng.ucsd.edu",
    description="SigProfilerTopographyCombiner combines separate SigProfilerTopography runs.",
    url="https://github.com/AlexandrovLab/SigProfilerTopographyCombiner",
    license='UCSD',
    packages=find_packages(),
    install_requires=[
        "SigProfilerTopography>=1.0.68",
	    "XlsxWriter>=1.3.7",
        "pandas>=1.1.5",
        "numpy>=1.20.1",
        "matplotlib>=2.2.2",
        "scipy>=1.1.0",
        "statsmodels>=0.9.0"],
    include_package_data=True,
	zip_safe=False)
