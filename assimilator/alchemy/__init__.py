import sqlalchemy

if sqlalchemy.__version__ < "2.0.0":
    raise RuntimeWarning(
        "PyAssimilator will only support SQLAlchemy 2 from now on. Please, update "
        "the library using this manual: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html"
    )
