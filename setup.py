from setuptools import find_packages, setup

setup(
    name='libname',
    packages=find_packages(include=['libname']),
    version='0.1.0',
    description='Mitsibushi robotics library',
    author='FunMetJoel',
    install_requires=['pyserial'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1', 'pytest-mock'],
    test_suite='tests',
)