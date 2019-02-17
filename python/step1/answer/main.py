#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Front end of Individual/Variant/Call API example
"""
import logging
import connexion
from connexion import NoContent
import yaml
from bravado_core.spec import Spec

SPEC = '../swagger.yaml'
#
# Bravado core can create Python classes from objects in the Swagger spec
#
SPEC_DICT = yaml.safe_load(open(SPEC, 'r'))
API_SPEC = Spec.from_dict(SPEC_DICT, config={'use_models': True})

Individual = API_SPEC.definitions['Individual']  # pylint:disable=invalid-name
Variant = API_SPEC.definitions['Variant']  # pylint:disable=invalid-name
Call = API_SPEC.definitions['Call']  # pylint:disable=invalid-name

#
# Example Individual, Variant, and Calls:
#
test_individual = Individual(id=1, description='Patient Zero')

test_variant = Variant(id=1, chromosome='chr1', start=14370,
                       ref='G', alt='A', name='rs6054257')

test_call = Call(id=1, variant_id=1, individual_id=1,
                 genotype='0/1', format='GQ:DP:HQ 48:1:51,51')

#
# in memory variant, individual 'database'
# TODO: calls
#
_variants = {1: test_variant}
_individuals = {1: test_individual}
_calls = {1: test_call}


#
# implement the endpoints
#
def get_variants(chromosome, start, end):
    """
    Return all variants between [chrom, start) and (chrom, end]
    """
    application.logger.info("inside get_variants")
    res = [var for var in _variants.values()
           if var.chromosome == chromosome
           and var.start >= start and var.start < end]
    return res, 200


def get_variant(variant_id):
    """
    Return a specific variant
    """
    application.logger.info("inside get_variant")
    if variant_id not in _variants:
        return NoContent, 404

    return _variants[variant_id], 200


def get_individuals():
    """
    Return all individuals
    """
    application.logger.info("inside get_individuals")
    return [ind for ind in _individuals.values()], 200


def get_individual(individual_id):
    """
    Return a specific indivdiual
    """
    if individual_id not in _individuals:
        return NoContent, 404
    return _individuals[individual_id], 200


def get_calls():
    """
    Return all calls
    """
    application.logger.info("inside get_calls")
    return [call for call in _calls.values()], 200


def get_call(call_id):
    """
    Return specific call
    """
    application.logger.info("inside get_call")
    if call_id not in _calls:
        return NoContent, 404

    return _calls[call_id], 200


def post_variant(variant):
    """
    Add a new variant
    """
    application.logger.info("Got variant: %s", str(variant))
    last_id = len(_variants)
    new_id = last_id + 1
    application.logger.info("assigned id: %d", new_id)

    variant['id'] = new_id
    _variants[new_id] = Variant(**variant)

    return NoContent, 201, {'Location': "/variants/"+str(new_id)}


def post_individual(individual):
    """
    Add a new individual
    """
    application.logger.info("Got individual: %s", str(individual))
    last_id = len(_individuals)
    new_id = last_id + 1
    application.logger.info("assigned id: %d", new_id)

    individual['id'] = new_id
    _individuals[new_id] = Individual(**individual)

    return NoContent, 201, {'Location': "/individuals/"+str(new_id)}


def post_call(call):
    """
    Add a new call
    """
    if call['variant_id'] not in _variants:
        application.logger.warn("Invalid call: %s", str(call))
        return NoContent, 405

    if call['individual_id'] not in _individuals:
        application.logger.warn("Invalid call: %s", str(call))
        return NoContent, 405

    last_id = len(_calls)
    new_id = last_id + 1

    call['id'] = new_id
    application.logger.info("Got call: %s", str(call))
    _calls[new_id] = Call(**call)
    return NoContent, 201, {'Location': "/calls/"+str(new_id)}


logging.basicConfig(level=logging.INFO)

app = connexion.FlaskApp(__name__)
app.add_api(SPEC)
application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):  # pylint: disable=unused-argument
    """
    cleanup
    """
    pass


if __name__ == '__main__':
    app.run(port=5000)
