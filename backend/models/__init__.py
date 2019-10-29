from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from libs.db import CustomQuery, base_model, DBSession


Base = declarative_base(cls=base_model(DBSession))
