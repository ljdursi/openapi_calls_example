#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Front end of Individual/Variant/Call API example
"""
import datetime
import logging

import connexion
from connexion import NoContent

from sqlalchemy import and_
import orm


def get_variants(chromosome, start, end):
    """
    Return all variants between [chrom, start) and (chrom, end]
    """
    q = db_session.query(orm.Variant)
    q = q.filter_by(chromosome=chromosome).filter(and_(start >= start, start <= end))
    return [orm.dump(p) for p in q]


def get_individuals():
    """
    Return all individuals
    """
    q = db_session.query(orm.Individual)
    return [orm.dump(p) for p in q]


def get_calls():
    """
    Return all calls
    """
    q = db_session.query(orm.Call)
    return [orm.dump(p) for p in q]


def put_variant(variant):
    """
    Add a new variant
    """
    vid = variant['id'] if 'id' in variant else None
    if vid is not None:
        if db_session.query(orm.Variant).filter(orm.Variant.id == vid).one_or_none():
            logging.info('Attempting to update existing variant %d..', vid)
            return NoContent, 405

    logging.info('Creating variant %d..', vid)
    variant['created'] = datetime.datetime.utcnow()
    db_session.add(orm.Variant(**variant))
    db_session.commit()
    return NoContent, 201


def put_individual(individual):
    """
    Add a new individual
    """
    iid = individual['id'] if 'id' in individual else None
    if iid is not None:
        if db_session.query(orm.Individual).filter(orm.Individual.id == iid).one_or_none():
            logging.info('Attempting to update individual %d..', iid)
            return NoContent, 405

    logging.info('Creating individual %d..', iid)
    individual['created'] = datetime.datetime.utcnow()
    db_session.add(orm.Individual(**individual))
    db_session.commit()
    return NoContent, 201


def put_call(call):
    """
    Add a new call
    """
    print(type(call))
    print(call)
    cid = call['id'] if 'id' in call else None
    if cid is not None:
        if db_session.query(orm.Call).filter(orm.Call.id == cid).one_or_none():
            logging.info('Attempting to update call %d..', cid)
            return NoContent, 405

    logging.info('Creating call %d..', cid)
    call['created'] = datetime.datetime.utcnow()
    db_session.add(orm.Call(**call))
    db_session.commit()
    return NoContent, 201


def get_variants_by_individual(ind_id):
    pass


def get_individuals_by_variant(var_id):
    pass


logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('sqlite:///:memory:')
app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml')

application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8080)
