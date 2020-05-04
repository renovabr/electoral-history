#!/usr/bin/env bash

YEARS=("2010" "2012" "2014" "2016" "2018")

function run_raw_data() {
  script="${1}"
  rawdata="${2}"

  cd src
  for i in "${YEARS[@]}"
  do
    p=`pwd`/../data/tse/${i}/${rawdata}${i}/
    echo "Importing ${p}"
	if [ ${i} == 2010 ] || [ ${i} == 2012 ]; then
	  python3 ${script} -y ${i} -p "${p}" -e txt
	else
	  python3 ${script} -y ${i} -p "${p}" -e csv	
    fi	
  done
  cd -
}

# run_raw_data "01-tse-consulta-cand.py" "consulta_cand_" &&
# run_raw_data "02-votacao-candidato-munzona.py" "votacao_candidato_munzona_" &&
# run_raw_data "03-votacao-partido-munzona.py" "votacao_partido_munzona_" &&

if [ $# -gt 0 ]; then
  if [ "${1}" == "consulta-cand" ]; then
    run_raw_data "01-consulta-cand.py" "consulta_cand_"
  elif [ "${1}" == "votacao-candidato" ]
  	run_raw_data "02-votacao-candidato-munzona.py" "votacao_candidato_munzona_"
  elif [ "${1}" == "votacao-partido" ]
    run_raw_data "03-votacao-partido-munzona.py" "votacao_partido_munzona_"
  else
    echo "Argument is not valid ${1}"
  fi
else
  echo "Add argument table import: consulta-cand | votacao-candidato | votacao-partido"
fi

exit 0