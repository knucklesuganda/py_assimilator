"""
That is the example for the people who are just starting with programming.
Some concepts like Dependency Injection are not followed here.

You will see how your code becomes easier step-by-step by using CRUDService pattern.
"""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float
from assimilator.core.usability.pattern_creator import create_crud
from assimilator.core.usability.registry import find_patterns


find_patterns('assimilator.alchemy')    # Import SQLAlchemy patterns

# Firstly, we need to create our User model. That code is just normal SQLAlchemy:
engine = create_engine(url="sqlite:///:memory:")
Base = declarative_base()


class AlchemyUser(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())
    balance = Column(Float())

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


Base.metadata.create_all(engine)
session_creator = sessionmaker(bind=engine)

# Now, we use PyAssimilator to create CRUDService pattern. It allows us to do Create/Read/Update/Delete operations
crud = create_crud(
    provider='alchemy',         # Provider is the external library that we are using. In our case - SQLAlchemy
    model=AlchemyUser,          # Model is the main entity that we will be working with.
    session=session_creator(),  # Session is the connection to the data source. In our case - SQLite
)


def create_user():
    # Now, let's create a function that will allow us to add a user
    new_user = crud.create({    # Create a user
        "username": "Andrey",
        "email": "python.on.papyrus@gmail.com",
        "balance": 1000000,
    })

    # The user is created! Let's print our username:
    print("Hello,", new_user.username)


def get_user():
    # Now, let's get a user using his username:
    user = crud.get(username="Andrey")  # We use crud.get() to retrieve a single user
    print(user.username, "has a balance of", user.balance)


"""
So, what did we do?

We created a CRUDService pattern that allows us to add a user to the database with:
    - No dependencies
    - Transaction management
    - Less code
    - Reproducibility

I hope you liked it and will use PyAssimilator in your projects!
"""


if __name__ == '__main__':
    create_user()
    get_user()
