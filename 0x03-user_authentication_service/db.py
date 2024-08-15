#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from sqlalchemy import select


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
        """Add a user to the db .
                """
        try:

            user = User()
            user.email = email
            user.hashed_password = hashed_password
            self._session.add(user)
            self._session.commit()

        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs):
        """
        Find user by given kwargs .
                """
        attributes = []
        values = []

        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            attributes.append(getattr(User, attr))
            values.append(val)

        # query = select(User).where(
        #     *(getattr(User, key) == value for key, value in kwargs.items())
        #     )
        # user = self._session.scalar(query)

        query = self._session.query(User)
        user = query.filter(tuple_(*attributes).in_([tuple(values)])).first()

        if not user:
            raise NoResultFound()

        return user
