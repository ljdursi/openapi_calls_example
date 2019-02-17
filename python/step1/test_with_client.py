#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Client for testing of Individual/Variant/Call API example
"""
import yaml
from bravado.client import SwaggerClient
from bravado.exception import HTTPNotFound, HTTPMethodNotAllowed

# read in API and generate HTTP client
SPEC_DICT = yaml.safe_load(open('swagger.yaml', 'r'))
SPEC_DICT['host'] = 'localhost:5000'

client = SwaggerClient.from_spec(SPEC_DICT)

Individual = client.get_model('Individual')
Variant = client.get_model('Variant')
Call = client.get_model('Call')

new_individual = Individual(id=2, description='Patient One')

new_variant = Variant(id=2, chromosome='chr2', start=51845108,
                      ref='C', alt='T', name='rs12994401')

new_call_1 = Call(id=2, variant_id=2, individual_id=1,
                  genotype='0/1', format='GQ:DP:HQ 48:1:51,51')

new_call_2 = Call(id=3, variant_id=1, individual_id=2,
                  genotype='0/1', format='GQ:DP:HQ 48:1:51,51')


def objs_equal(obj1, obj2, attrs):
    """
    Test to see if two objects have equality in all provided attributes
    """
    for attr in attrs:
        if getattr(obj1, attr) != getattr(obj2, attr):
            return False
    return True


def calls_equal(call1, call2):
    "Test to see if two calls have equality in all key attributes"
    attrs = ('variant_id', 'individual_id', 'genotype', 'format')
    return objs_equal(call1, call2, attrs)


def variants_equal(var1, var2):
    "Test to see if two variants have equality in all key attributes"
    attrs = ('name', 'ref', 'alt', 'chromosome', 'start')
    return objs_equal(var1, var2, attrs)


def individuals_equal(ind1, ind2):
    "Test to see if two variants have equality in all key attributes"
    attrs = ('description', )
    return objs_equal(ind1, ind2, attrs)


def test_get_variants_none():
    """
    Searching on an invalid chromosome - should always return nothing
    """
    res = client.variants.get_variants(chromosome='chr123',
                                       start=1, end=100000).response()
    res = res.result
    assert len(res) == 0, "Found a variant on chromosome 123!"


def test_get_individuals():
    """
    Make sure there's valid response from get_individuals
    """
    response = client.individuals.get_individuals().response().result
    assert response is not None, "Null response from get individuals"


def test_get_invalid_individual():
    """
    Make sure we can't find an individual that doesn't exist
    """
    try:
        res = client.individuals.get_individual(individual_id=99999)\
            .response().result
    except HTTPNotFound:
        return

    assert False, "Found nonexistant individual 99999"


def test_insert_individuals():
    """
    Post a new individual, and then:
        - make sure the individual shows up in get_individuals
        - make sure we can get that specific individual by id
    """
    res = client.individuals.post_individual(individual=new_individual).response()
    http_response = res.incoming_response
    res = res.result

    newid = int(http_response.headers['Location'].split('/')[-1])
    res = client.individuals.get_individuals().response().result
    found = False
    for item in res:
        if individuals_equal(item, new_individual):
            found = True
    assert found, "Posted individual not in list of all individuals"

    res = client.individuals.get_individual(individual_id=newid).response().result
    assert individuals_equal(res, new_individual), \
           "Retrieved individual different from posted individual"


def test_insert_variants():
    """
    Post a new variant, and then:
        - make sure the individual shows up in get_individuals
        - make sure we can get that specific individual by id
    """
    res = client.variants.post_variant(variant=new_variant).response()
    http_response = res.incoming_response
    res = res.result
    
    newid = int(http_response.headers['Location'].split('/')[-1])
    res = client.variants.get_variants(chromosome=new_variant.chromosome,
                                       start=new_variant.start-100,
                                       end=new_variant.start+100).response().result
    found = False
    for item in res:
        if variants_equal(item, new_variant):
            found = True
    assert found, "Posted variant not in list of all variants"

    res = client.variants.get_variant(variant_id=newid).response().result
    assert variants_equal(res, new_variant), \
        "Retrieved variant differes from posted variant"


def test_get_invalid_variant():
    """
    Make sure we can't find a variant that doesn't exist
    """
    try:
        _ = client.variants.get_variant(variant_id=99999)\
            .response().result
    except HTTPNotFound:
        return

    assert False, "Found nonexistant variant 99999"


def test_get_calls():
    """
    Make sure get_calls has valid response
    """
    res = client.calls.get_calls().response().result
    assert res is not None, "Null response from get calls"


def test_insert_calls():
    newids = []
    for new_call in [new_call_1, new_call_2]:
        res = client.calls.post_call(call=new_call).response()
        http_response = res.incoming_response
        newids.append(int(http_response.headers['Location'].split('/')[-1]))

    res = client.calls.get_calls().response().result
    found = []
    for new_call in [new_call_1, new_call_2]:
        ifound = False
        for call in res:
            if calls_equal(call, new_call):
                ifound = True
        found.append(ifound)
    assert all(found), "New posted calls not found in list of all calls"

    for new_id, new_call in zip(newids, [new_call_1, new_call_2]):
        res = client.calls.get_call(call_id=new_id).response().result
        assert calls_equal(new_call, res), "Newly posted call differed from returned call"


def test_insert_invalid_call():
    """
    Try inserting a call connecting a valid variant
    to an individual who doesn't exist
    """
    new_call_1.individual_id = 99999
    try:
        _ = client.calls.post_call(call=new_call_1).response().result
    except HTTPMethodNotAllowed:
        return

    assert False, "Post of call referncing invalid individual should have failed"


def test_get_invalid_call():
    """
    Make sure we can't find an invalid call
    """
    try:
        _ = client.calls.get_call(call_id=99999)\
            .response().result
    except HTTPNotFound:
        return

    assert False, "Found nonexistant call 99999"
