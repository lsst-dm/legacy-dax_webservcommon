from setuptools import setup

requires = [
    'flask'
]

setup(
    name='webcommon',
    #namespace_packages = ["lsst"],
    version='0.1',
    package_dir={'lsst': 'python/lsst'},
    package_data={'lsst': ['webcommon/templates/*.html']},
    packages=['lsst', 'lsst.webcommon'],
    license='',
    zip_safe=False,
    install_requires=requires
)
