#!/usr/bin/env python3
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=redefined-builtin
"""
Database layer for Individuals/Variants/Calls API
"""
import os
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def dump(obj):
    """
    Generate list of fields without SQLAlchemy internal fields & relationships
    """
    return dict([(k, v) for k, v in vars(obj).items()
                 if not k.startswith('_')])


class Individual(Base):
    """
    SQLAlchemy class/table representing an individual
    """
    __tablename__ = 'individuals'
    id = Column(Integer, primary_key=True)
    description = Column(String(100))
    created = Column(DateTime())


class Variant(Base):
    """
    SQLAlchemy class/table representing a Variant
    """
    __tablename__ = 'variants'
    id = Column(Integer, primary_key=True)
    chromosome = Column(String(10))
    start = Column(Integer)
    ref = Column(String(100))
    alt = Column(String(100))
    name = Column(String(100))
    created = Column(DateTime())


class Call(Base):
    """
    SQLAlchemy class/table representing Calls
    """
    __tablename__ = 'calls'
    id = Column(Integer, primary_key=True)
    individual_id = Column(String(20), ForeignKey('individuals.id'))
    variant_id = Column(String(20), ForeignKey('variants.id'))
    genotype = Column(String(20))
    fmt = Column(String(100))
    created = Column(DateTime())


def init_db(uri):
    """
    Start the database session
    """
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session


#
# test/example run
#
if __name__ == "__main__":
    db_filename = "test.db"
    # delete db if already exists
    try:
        os.remove(db_filename)
    except OSError:
        pass

    session = init_db('sqlite:///'+db_filename)

    ind1 = Individual(id=1, description='Subject X')
    ind2 = Individual(id=7, description='Subject Y')

    variant1 = Variant(id=1, name='rs699', chromosome='chr1', start=230710048, ref='C', alt='T')
    variant2 = Variant(id=2, name='rs900', chromosome='chr1', start=218441563, ref='A', alt='T')
    variant3 = Variant(id=3, name='rs5714', chromosome='chr1', start=53247055, ref='A', alt='G')

    call1 = Call(id=1, individual_id=1, variant_id=1, genotype='0/1')
    call2 = Call(id=2, individual_id=1, variant_id=2, genotype='0/0')
    call3 = Call(id=3, individual_id=7, variant_id=2, genotype='1/1')
    call4 = Call(id=4, individual_id=7, variant_id=3, genotype='0/1')

    session.add_all([ind1, ind2, variant1, variant2, variant3, call1, call2, call3, call4])
    session.commit()
