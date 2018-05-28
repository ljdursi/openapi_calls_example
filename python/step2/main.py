#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Front end of Individual/Variant/Call API example
"""
import datetime
import logging

import connexion
from connexion import NoContent


def get_variants(chromosome, start, end):
    """
    Return all variants between [chrom, start) and (chrom, end]
    """
    print("get_variants", chromosome, start, end)
    return NoContent, 200


def get_individuals():
    """
    Return all individuals
    """
    print("get_individuals")
    return NoContent, 200


def get_calls():
    """
    Return all calls
    """
    print("get_calls")
    return NoContent, 200


def put_variant(variant):
    """
    Add a new variant
    """
    print("Supposed to be putting variant in: ")
    print(variant)
    return NoContent, 201


def put_individual(individual):
    """
    Add a new individual
    """
    print("Supposed to be putting individual  in: ")
    print(individual)
    return NoContent, 201


def put_call(call):
    """
    Add a new call
    """
    print("Supposed to be putting call  in: ")
    print(call)
    return NoContent, 201


logging.basicConfig(level=logging.INFO)

app = connexion.FlaskApp(__name__)
app.add_api('swagger.yaml')

application = app.app

@application.teardown_appcontext
def shutdown_session(exception=None):
    """
    cleanup
    """
    pass


if __name__ == '__main__':
    app.run(port=8080)
