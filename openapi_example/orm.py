#!/usr/bin/env python3

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

Base = declarative_base()


class Individual(Base):
    __tablename__ = 'individuals'
    id = Column(Integer, primary_key=True)
    description = Column(String(100))
    created = Column(DateTime())
    calls = relationship("Call", back_populates="individual")

    def update(self, id=None, description=None, created=None):
        if id is not None:
            self.id = id
        if description is not None:
            self.description = description
        if created is not None:
            self.created = created

    def dump(self):
        """ Remove SQLAlchemy internal fields and the relationship fields """
        return dict([(k, v) for k, v in vars(self).items()
                     if not k.startswith('_') and not k=="calls"])


class Variant(Base):
    __tablename__ = 'variants'
    id = Column(Integer, primary_key=True)
    chromosome = Column(String(10))
    start = Column(Integer)
    ref = Column(String(100))
    alt = Column(String(100))
    name = Column(String(100))
    created = Column(DateTime())
    calls = relationship("Call", back_populates="variant")

    def update(self, id=None, chromosome=None, start=None, ref=None, alt=None,
               name=None, created=None):
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if chromosome is not None:
            self.chromosome = chromosome
        if start is not None:
            self.start = start
        if ref is not None:
            self.ref = ref
        if alt is not None:
            self.alt = alt
        if created is not None:
            self.created = created

    def dump(self):
        """ Remove SQLAlchemy internal fields and the relationship fields """
        return dict([(k, v) for k, v in vars(self).items()
                     if not k.startswith('_') and not k=="calls"])


class Call(Base):
    __tablename__ = 'calls'
    id = Column(Integer, primary_key=True)
    individual_id = Column(String(20), ForeignKey('individuals.id'))
    individual = relationship("Individual", back_populates="calls")
    variant_id = Column(String(20), ForeignKey('variants.id'))
    variant = relationship("Variant", back_populates="calls")
    genotype = Column(String(20))
    fmt = Column(String(100))
    created = Column(DateTime())

    def update(self, id, variant_id, individual_id, genotype,
               fmt=None, created=None):
        if id is not None:
            self.id = id
        self.variant_id = variant_id
        self.individual_id = individual_id
        self.genotype = genotype
        if fmt is not None:
            self.fmt = fmt
        if created is not None:
            self.created = created

    def dump(self):
        """ Remove SQLAlchemy internal fields and the relationship fields """
        return dict([(k, v) for k, v in vars(self).items()
                     if not k.startswith('_') and k not in ['variant', 'individual']])


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session


if __name__ == "__main__":
    session = init_db('sqlite:///test.db')
    ind1 = Individual(id=1, description='Subject X')
    ind2 = Individual(id=7, description='Subject Y')
    variant1 = Variant(id=1, name='rs699', chromosome='chr1', start=230710048, ref='C', alt='T')
    variant2 = Variant(id=2, name='rs900', chromosome='chr1', start=218441563, ref='A', alt='T')
    variant3 = Variant(id=3, name='rs5714', chromosome='chr1', start=53247055, ref='A', alt='G')
    call1 = Call(id=1, individual_id=1, variant_id=1, genotype='0/1')
    call2 = Call(id=2, individual_id=1, variant_id=2, genotype='0/0')
    call3 = Call(id=3, individual_id=7, variant_id=2, genotype='1/1')
    call4 = Call(id=4, individual_id=7, variant_id=3, genotype='0/1')
    call5 = Call(individual_id=7, variant_id=1, genotype='1/1')

    session.add_all([ind1, ind2, variant1, variant2, variant3, call1, call2, call3, call4, call5])
    session.commit()

    print([call.dump() for call in ind2.calls])
    print([call.dump() for call in variant2.calls])

    ind1variants = [call.variant for call in ind1.calls if call.variant is not None]
    print([v.dump() for v in ind1variants])

    variant2inds = [call.individual for call in variant2.calls if call.individual is not None]
    print([i.dump() for i in variant2inds])
