from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(url="sqlite:///:memory:", echo="debug")
DatabaseSession = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())
    balance = Column(Float())

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


Base.metadata.create_all(engine)

__all__ = ['User', 'DatabaseSession']
