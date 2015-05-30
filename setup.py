from setuptools import setup

requires = [
    'flask'
]

setup(
    name='webservcommon',
    #namespace_packages = ["lsst"],
    version='0.1',
    package_dir={'lsst': 'python/lsst'},
    package_data={'lsst': ['webservcommon/templates/*.html']},
    packages=['lsst', 'lsst.webservcommon'],
    license='',
    zip_safe=False,
    install_requires=requires
)
