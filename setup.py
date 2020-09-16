import os
from setuptools import setup, find_packages

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()

# Dependencies (format is 'PYPI_PACKAGE_NAME[>=]=VERSION_NUMBER')
BASE_DEPENDENCIES = [
    'psutil>=5.7.2',
    'click>=7.1.2'
]

# TEST_DEPENDENCIES = [
# ]
#
# LOCAL_DEPENDENCIES = [
# ]

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))

setup(
    name='wf-rpi-monitor',
    packages=find_packages(),
    version=VERSION,
    include_package_data=True,
    description='Tools to monitor and log status of a Raspberry Pi',
    long_description=open('README.md').read(),
    url='https://github.com/WildflowerSchools/wf-rpi-monitor',
    author='Theodore Quinn',
    author_email='ted.quinn@wildflowerschools.org',
    install_requires=BASE_DEPENDENCIES,
    # tests_require=TEST_DEPENDENCIES,
    # extras_require = {
    #     'test': TEST_DEPENDENCIES,
    #     'local': LOCAL_DEPENDENCIES
    # },
    entry_points='''
        [console_scripts]
        log_rpi_status=rpi_monitor.workers:log_rpi_status
        fibonacci_test=rpi_monitor.workers:fibonacci_test
        sleep_test=rpi_monitor.workers:sleep_test
    ''',
    keywords=['rpi'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: IRIX',
        'Programming Language :: Python',
    ]
)
