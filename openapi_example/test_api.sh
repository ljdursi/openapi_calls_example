#!/bin/bash -x

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

function main {
    add_individual "Subject X" 1
    add_individual "Subject Y" 7

    get_individuals

    add_variant 'chr1' 230710048 'C' 'T' 'rs699' 1
    add_variant 'chr1' 218441563 'A' 'T' 'rs900' 2 
    add_variant 'chr1' 53247055 'A' 'G' 'rs5714' 3 

    get_variants
}

main

#    call1 = Call(id=1, individual_id=1, variant_id=1, genotype='0/1')
#    call2 = Call(id=2, individual_id=1, variant_id=2, genotype='0/0')
#    call3 = Call(id=3, individual_id=7, variant_id=2, genotype='1/1')
#    call4 = Call(id=4, individual_id=7, variant_id=3, genotype='0/1')
