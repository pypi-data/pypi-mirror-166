from setuptools import setup

setup(
    name='kih_api',
    version='0.9.2',
    url='https://github.com/Kontinuum-Investment-Holdings/KIH_API',
    author='Kavindu Athaudha',
    author_email='kavindu@k-ih.co.uk',
    packages=['kih_api'],
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "urllib3",
        "pytz",
        "python-dateutil",
        "pandas",
        "numpy",
        "ibapi",
        "validators",
        "dacite",
        "mongoengine",
        "pymongo",
        "dataclass_csv"
    ]
)
