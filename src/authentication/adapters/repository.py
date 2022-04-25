from typing import Set
import uuid
import abc

from authentication.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.User]

    def add(self, user: model.User):
        self._add(user)
        self.seen.add(user)

    def get(self, username: str) -> model.User:
        user = self._get(username)
        if user:
            self.seen.add(user)
        return user

    def get_by_id(self, id: uuid.uuid4) -> model.User:
        user = self._get_by_id(id)
        if user:
            self.seen.add(user)
        return user

    @abc.abstractmethod
    def _add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, username: str) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: uuid.uuid4) -> model.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self._session = session

    def _add(self, user):
        self._session.add(user)

    def _get(self, username):
        return self._session.query(model.User).filter_by(username=username).first()

    def _get_by_id(self, id):
        return self._session.query(model.User).filter_by(id=id).first()
