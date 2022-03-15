from setuptools import setup
TEST_REQUIREMENTS = [
    'pytest',
    'pytest-django',
    'pylint',
    'pylint_django',
    'git-pylint-commit-hook',
]

INSTALL_REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
setup(
    name='journeysharing',
    version='0.1.0',
    description='A backend service for handling journey related request.',
    author='Rakesh Nair, Conor Church, Ankana Bhattacharjee, Vishnu Priya',
    author_email='ranair@tcd.ie, churchco@tcd.ie, bhattaa1@tcd.ie, uppalapv@tcd.ie',
    packages=['journeysharing'],
    license='Apache Software License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=['pytest-runner'],
    tests_require=TEST_REQUIREMENTS,
)