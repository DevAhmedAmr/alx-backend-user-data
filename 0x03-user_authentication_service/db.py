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
from sqlalchemy import and_
from sqlalchemy import update


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

    def find_All_Users(self) -> User:
        """
        find_All_Users

        Returns:
            [Users]
        """
        query = select(User)
        result = self._session.execute(query)
        users = result.scalars().all()
        print(users)
        return users

    def find_user_by(self, **kwargs) -> User:
        """
        Find user by given kwargs .
                """
        attributes = []
        values = []

        for att, value in kwargs.items():

            if not hasattr(User, att):
                raise InvalidRequestError()
            attributes.append(att)
            values.append(value)

        # query = select(User).where(
        #     *(getattr(User, key) == value for key, value in kwargs.items())
        #     )
        # user = self._session.scalar(query)

        query = self._session.query(User)

        conditions = [
            getattr(User, key) == value for key,
            value in kwargs.items()
        ]

        user = query.filter(*conditions).first()

        if not user:
            raise NoResultFound()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user by ID .

        Args:
            user_id (int): id of user to be updated
            **kwargs: attributes to be updated
        Raises:
            ValueError: if attribute to be updated does not exist
            in User table

        Returns:
            None
        """
        user = self.find_user_by(**{"id": user_id})
        session = self._session

        for attr, value in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError
            user.__setattr__(attr, value)

        session.commit()
        return None
