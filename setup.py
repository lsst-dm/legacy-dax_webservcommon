from setuptools import setup

requires = [
    'flask',
    'jinja2'
]

setup(
    name='webservcommon',
    version='0.1',
    package_dir={'lsst': 'python/lsst'},
    package_data={'lsst': ['dax/webservcommon/templates/*.html']},
    packages=['lsst', 'lsst.dax.webservcommon'],
    zip_safe=False,
    install_requires=requires
)
