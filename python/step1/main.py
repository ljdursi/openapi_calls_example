#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Front end of Individual/Variant/Call API example
"""
import datetime
import logging
import connexion
import yaml
from connexion import NoContent
from bravado_core.spec import Spec

#
# Bravado core can create Python classes from objects in the Swagger spec
#
SPEC_DICT = yaml.safe_load(open('swagger.yaml', 'r'))
SWAGGER_SPEC = Spec.from_dict(SPEC_DICT, config={'use_models': True})

Individual = SWAGGER_SPEC.definitions['Individual']  # pylint:disable=invalid-name
Variant = SWAGGER_SPEC.definitions['Variant']  # pylint:disable=invalid-name
Call = SWAGGER_SPEC.definitions['Call']  # pylint:disable=invalid-name

#
# Example Individual, Variant, and Calls:
#
test_individual = Individual(id=1, description='Patient Zero',
                             created=datetime.datetime.now())

test_variant = Variant(id=1, chromosome='chr1', start=14370,
                       ref='G', alt='A', name='rs6054257',
                       created=datetime.datetime.now())

test_call = Call(id=1, variant_id=1, individual_id=1,
                 genotype='0/1', format='GQ:DP:HQ 48:1:51,51',
                 created=datetime.datetime.now())

def get_variants(chromosome, start, end):
    """
    Return all variants between [chrom, start) and (chrom, end]
    """
    logging.info("inside get_variants")
    return [test_variant], 200


def get_individuals():
    """
    Return all individuals
    """
    logging.info("inside get_individuals")
    return [test_individual], 200


def get_calls():
    """
    Return all calls
    """
    print("get_calls")
    logging.info("inside get_calls")
    return [test_call], 200


def post_variant(variant):
    """
    Add a new variant
    """
    logging.info("Got variant: %s", str(variant))
    return NoContent, 201


def post_individual(individual):
    """
    Add a new individual
    """
    logging.info("Got individual: %s", str(individual))
    return NoContent, 201


def post_call(call):
    """
    Add a new call
    """
    logging.info("Got call: %s", str(call))
    return NoContent, 201


logging.basicConfig(level=logging.INFO)

app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml', strict_validation=False)

application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    """
    cleanup
    """
    pass


if __name__ == '__main__':
    app.run(port=5000)
