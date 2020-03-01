from setuptools import find_packages, setup

setup(
    name='mudpp',
    version='0.9.7',
    packages=find_packages(),
    include_package_data=True,
    package_data={'mudpp': [ 'templates/*.html' ]},
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
