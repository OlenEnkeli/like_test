from typing import Type
from math import ceil

from sqlalchemy import inspect, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from config import config


DEFAULT_PAGE_SIZE = 40


class CustomQuery(Query):

    def paginate(self, page_number: int, page_size: int):
        return self.limit(page_size).offset(
            (page_number - 1) * page_size
        )

    def total(self):
        return self.order_by(None).count()

    def fetch_assoc(self):
        results = []
        data = self.session.execute(self).fetchall()
        if len(data) == 0:
            return results

        for row_number, row in enumerate(data):
            results.append({})
            for column_number, value in enumerate(row):
                results[row_number][row.keys()[column_number]] = value

        return results


class Pagination:

    __slots__ = ['query', 'page', 'page_size']

    def __init__(self, query: CustomQuery, page: int, page_size: int):
        self.query = query
        self.page = page
        self.page_size = page_size

    @property
    def items(self):
        return self.query.paginate(
            self.page,
            self.page_size
        ).all()

    @property
    def total_pages(self):
        return ceil(self.query.total() / self.page_size) or 1

    @property
    def total(self):
        return self.query.total()


class Model:

    filter_field = None
    desc = False

    def update(self, params: dict):

        for key, value in params.items():
            setattr(self, key, value)

    def save(self):

        self.db_session.add(self)
        return self

    def delete(self):

        self.db_session.delete(self)

    def commit(self):

        self.db_session.commit()

    def flush(self):

        self.db_session.flush()

    def to_dict(self):

        return dict((prop.key, getattr(self, prop.key))
                    for prop in inspect(self).mapper.iterate_properties)

    @classmethod
    def is_exists(cls, model_id: int = None, **fields):

        filters = {'id': model_id} if model_id else fields

        return cls.db_session.query(
            cls.db_session.query(cls)
            .filter_by(**filters)
            .exists()
        ).scalar()

    @classmethod
    def exists_or_not_found(cls, model_id: int = None, **fields):

        if cls.is_exists(model_id, **fields):
            return

        raise NoResultFound({'error_message': 'No row was found by id'})

    @classmethod
    def get_or_not_found(cls, model_id: int):

        query = cls.query \
                .filter(cls.id == model_id)
        if "deleted" in cls.__dict__:
            query = query.filter(cls.deleted.is_(False))
        model = (
            query.limit(1).first()
        )
        if model is None:
            raise NoResultFound({'error_message': 'No row was found by id'})

        return model

    @hybrid_property
    def query(self):

        return self.db_session.query(self)

    @classmethod
    def filters(cls, query=None, **params):

        query = query or cls.query

        filter_field = getattr(cls, cls.filter_field, None) if cls.filter_field is not None\
            else getattr(cls, 'name', None)
        if filter_field is not None:
            if cls.desc:
                query = query.order_by(filter_field.desc())
            else:
                query = query.order_by(filter_field)

        for key, value in params.items():
            is_not_valid_filter = (
                    not hasattr(cls, key) or
                    value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(cls, key, None)

            if isinstance(value, str):
                query = query.filter(field.ilike('%{}%'.format(value)))
            else:
                query = query.filter(field == value)

        return query

    @classmethod
    def get_by_filters(cls,
                       query=None,
                       page: int = 1,
                       page_size: int = DEFAULT_PAGE_SIZE,
                       **params: dict):

        query = query or cls.query
        return Pagination(
            query=cls.filters(query=query, **params),
            page=page,
            page_size=page_size
        )


class AdditionalFilters(Model):

    @classmethod
    def rev_filters(cls, query: CustomQuery, **params) -> CustomQuery:

        for key, value in params.items():
            is_not_valid_filter = (
                    not hasattr(cls, key) or
                    value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(cls, key, None)

            query = query.filter(field != value)

        return query

    @classmethod
    def get_by_filters(cls,
                       page: int = 1,
                       page_size: int = DEFAULT_PAGE_SIZE,
                       rev_filters=None,
                       **params: dict):
        if rev_filters is None:
            rev_filters = {}
        return Pagination(
            query=cls.rev_filters(cls.filters(**params), **rev_filters),
            page=page,
            page_size=page_size
        )


def base_model(session: scoped_session):

    class BaseModel(Model):
        db_session = session

    return BaseModel


def with_pagination_meta(models: list, pagination: Pagination):

    return {
        'data': models,
        'meta': {
            'current_page': pagination.page,
            'total_pages': pagination.total_pages,
            'page_size': pagination.page_size
        }
    }


engine = create_engine(
    'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**config['db'])
)

DBSession = scoped_session(sessionmaker(bind=engine, query_cls=CustomQuery))


class SQLAlchemySessionManager:

    def __init__(self):
        self.db_session = DBSession

    def process_resource(self, req, resp, resource, params):
        resource.db_session = self.db_session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            resource.db_session.remove()
