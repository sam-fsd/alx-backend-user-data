"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        user = self._session.query(User).filter_by(email=email).first()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the given criteria.

        Args:
            **kwargs: Keyword arguments representing the criteria to
                      search for.
                      The keys should correspond to attributes of the
                      User class.

        Returns:
            User: The found user.

        Raises:
            InvalidRequestError: If any of the provided criteria is not a valid
            attribute of the User class.
            NoResultFound: If no user is found matching the provided criteria.
        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError
        email = kwargs.get('email')
        user = self._session.query(User).filter_by(email=email).first()
        if user is None:
            raise NoResultFound
        return user