from setuptools import setup

setup(
    name='webservcommon',
    package_dir={'lsst': 'python/lsst'},
    package_data={'lsst': ['dax/webservcommon/templates/*.html']},
    packages=['lsst', 'lsst.dax.webservcommon'],
    zip_safe=False,
    use_scm_version=True
)
