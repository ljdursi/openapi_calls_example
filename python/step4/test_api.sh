#!/bin/bash

readonly DEFBASEURL="http://localhost:8080"
readonly SENDJSON="Content-type: application/json"
readonly GETJSON="Accept: application/json"

function add_individual {
    local desc=$1
    local id=${2:-"None"}
    local baseurl=${3:-${DEFBASEURL}}
    local ENDPOINT="/individuals"

    local xmit="\"description\": \"${desc}\""
    if [[ "${id}" == "None" ]]
    then
        xmit="{ $xmit }"
    else
        xmit="{ \"id\": ${id}, $xmit }"
    fi

    local url=${baseurl}${ENDPOINT}
    curl -X PUT --url "${url}" -H "${SENDJSON}" -H "${GETJSON}" --data "${xmit}"
}

function get_individuals {
    local baseurl=${1:-${DEFBASEURL}}
    local ENDPOINT="/individuals"
    local url=${baseurl}${ENDPOINT}

    curl --url "${url}" -H "${GETJSON}"
}

function add_variant {
    local chrom=$1
    local start=$2
    local ref=$3
    local alt=$4
    local name=${5:-"None"}
    local id=${6:-"None"}
    local baseurl=${7:-${DEFBASEURL}}
    local ENDPOINT="/variants"

    local xmit="\"chromosome\": \"${chrom}\", \"start\": ${start}, \"ref\": \"${ref}\", \"alt\": \"${alt}\""
    if [[ "${name}" != "None" ]]
    then
        xmit=${xmit}", \"name\": \"${name}\""
    fi
    if [[ "${id}" != "None" ]]
    then
        xmit=${xmit}", \"id\": ${id}"
    fi

    local url=${baseurl}${ENDPOINT}
    curl -X PUT --url "${url}" -H "${SENDJSON}" -H "${GETJSON}" --data "{ ${xmit} }"
}

function get_variants {
    local chrom=${1:-"chr1"}
    local start=${2:-1}
    local end=${3:-53247056}
    local baseurl=${4:-${DEFBASEURL}}

    local ENDPOINT="/variants"
    local url=${baseurl}${ENDPOINT}

    url="${url}?chromosome=${chrom}&start=${start}&end=${end}"

    curl --url "${url}" -H "${GETJSON}"
}

function add_call {
    local individual_id=$1
    local variant_id=$2
    local genotype=$3
    local format=${4:-"None"}
    local id=${5:-"None"}
    local baseurl=${6:-${DEFBASEURL}}

    local ENDPOINT="/calls"
    local url=${baseurl}${ENDPOINT}

    local xmit="\"individual_id\": ${individual_id}, \"variant_id\": ${variant_id}"
    local xmit="${xmit}, \"genotype\": \"${genotype}\""
    if [[ "${format}" != "None" ]]
    then
        xmit=${xmit}", \"format\": \"${format}\""
    fi
    if [[ "${id}" != "None" ]]
    then
        xmit=${xmit}", \"id\": ${id}"
    fi

    curl -X PUT --url "${url}" -H "${SENDJSON}" -H "${GETJSON}" --data "{ ${xmit} }"
}

function get_calls {
    local baseurl=${1:-${DEFBASEURL}}
    local ENDPOINT="/calls"
    local url=${baseurl}${ENDPOINT}

    curl --url "${url}" -H "${GETJSON}"
}

function get_variants_by_individual {
    local individual_id=$1
    local baseurl=${2:-${DEFBASEURL}}
    local ENDPOINT="/variants/by_individual"

    local url="${baseurl}${ENDPOINT}/${individual_id}"

    curl --url "${url}" -H "${GETJSON}"
}

function get_individuals_by_variant {
    local variant_id=$1
    local baseurl=${2:-${DEFBASEURL}}
    local ENDPOINT="/individuals/by_variant"

    local url="${baseurl}${ENDPOINT}/${variant_id}"

    curl --url "${url}" -H "${GETJSON}"
}

function main {
    add_individual "Subject X" 1
    add_individual "Subject Y" 7

    echo "Individuals in db:"
    get_individuals
    echo ""

    add_variant 'chr1' 230710048 'C' 'T' 'rs699' 1
    add_variant 'chr1' 218441563 'A' 'T' 'rs900' 2 
    add_variant 'chr1' 53247055 'A' 'G' 'rs5714' 3 

    echo "Variants in db:"
    get_variants
    echo ""

    add_call 1 1 '0/1'
    add_call 1 2 '0/0'
    add_call 7 2 '1/1'
    add_call 7 3 '0/1'

    echo "Calls in db:"
    get_calls
    echo ""

    echo "Variants in individual 7:"
    get_variants_by_individual 7

    echo "Individuas with variant 2:"
    get_individuals_by_variant 2
}

main
