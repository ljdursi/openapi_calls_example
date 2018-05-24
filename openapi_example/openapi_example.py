#!/usr/bin/env python3
import datetime
import logging

import connexion
from connexion import NoContent

from sqlalchemy import and_
import orm

db_session = None


def get_variants(chrom, start, end):
    q = db_session.query(orm.Variant)
    q = q.filter_by(chromosome == chromosome).filter(and_(start >= start, start <= end))
    return [p.dump() for p in q]


def put_variant(variant):
    variant_id = variant.id
    v = db_session.query(orm.Variant).filter(orm.Variant.id == variant_id).one_or_none()
    if p is not None:
        logging.info('Updating variant %s..', variant_id)
        p.update(**variant)
    else:
        logging.info('Creating variant %s..', variant_id)
        variant['created'] = datetime.datetime.utcnow()
        db_session.add(orm.Variant(**variant))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def get_individuals():
    q = db_session.query(orm.Individual)
    return [p.dump() for p in q]


def put_individual(individual):
    individual_id = individual.id
    v = db_session.query(orm.Variant).filter(orm.Variant.id == individual_id).one_or_none()
    if p is not None:
        logging.info('Updating individual %s..', individual_id)
        p.update(**individual)
    else:
        logging.info('Creating individual %s..', individual_id)
        individual['created'] = datetime.datetime.utcnow()
        db_session.add(orm.Individual(**individual))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def get_individuals():
    q = db_session.query(orm.Individual)
    return [p.dump() for p in q]


def put_individual(individual):
    individual_id = individual.id
    v = db_session.query(orm.Variant).filter(orm.Variant.id == individual_id).one_or_none()
    if p is not None:
        logging.info('Updating individual %s..', individual_id)
        p.update(**individual)
    else:
        logging.info('Creating individual %s..', individual_id)
        individual['created'] = datetime.datetime.utcnow()
        db_session.add(orm.Individual(**individual))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


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
