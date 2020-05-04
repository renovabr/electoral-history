#!/usr/bin/env bash

URL='http://agencia.tse.jus.br/estatistica/sead/odsele/'

function base_dir() {
  base=data/tse/"${1}"
  [[ -d ${base} ]] || mkdir -p ${base}
}

function get_cand_data() {
  year="${1}"
  base=data/tse/${year}

  data=("consulta_cand/consulta_cand_${year}.zip")

  for i in "${data[@]}"
  do
    echo "${URL}$i"
    wget -N -P ${base} "${URL}${i}" 
  done
}

function get_vot_data() {
  year="${1}"
  base=data/tse/${year}

  data=("votacao_candidato_munzona/votacao_candidato_munzona_${year}.zip" 
    "votacao_partido_munzona/votacao_partido_munzona_${year}.zip")

  for i in "${data[@]}"
  do
    echo "${URL}$i"
    wget -N -P ${base} "${URL}${i}" 
  done      
}

[[ "$(command -v wget)" ]] || { echo "Sorry! Command (wget) is not installed...." 1>&2 && exit -1; }

if [ $# -gt 0 ]; then
  if [ "${1}" == "2010" ] || 
    [ "${1}" == "2012" ] || [ "${1}" == "2014" ] || 
    [ "${1}" == "2016" ] || [ "${1}" == "2018" ]; then
    echo "YEAR is valid ${1}"
  else
    echo "YEAR is not valid ${1}"
  fi
  base_dir "${1}" &&
  get_cand_data "${1}" &&
  get_vot_data "${1}"
else
  echo "Add argument YEAR eg: 2010 2012 2014 2016 2018"
fi

exit 0
