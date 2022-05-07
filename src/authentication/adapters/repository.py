import abc
import uuid

from authentication.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, username: str) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, id: uuid.uuid4) -> model.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self._session = session

    def add(self, user):
        self._session.add(user)

    def get(self, username):
        return self._session.query(model.User).filter_by(username=username).first()

    def get_by_id(self, id):
        return self._session.query(model.User).filter_by(id=id).first()
