#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os.path

from sqlalchemy import create_engine
conn = 'mysql+mysqlconnector://winston:cj#hCx0@R3$@gm@localhost:3307/electoral_history'


YEAR = '2016'
VOTACAO_ZONA_PATH = "/home/edmc/Downloads/2016-original-tse/votacao_candidato_munzona_" + YEAR + "/"

STATES = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    # "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO"
]

"""
STATES = [
    "RN",
]
"""

def main():
    engine = create_engine(conn, echo=False)
    
    df = pd.read_sql("""
      SELECT
        nm_city,
        sq_candidate,
        ds_position,
        cd_position,
        ds_situ_tot_shift,
        qt_votes_nominal 
      FROM
        raw_tse_voting_cand_city 
      WHERE
        election_year = '2016' 
        AND sg_uf = 'AC' 
        AND cd_position = 13""", engine)

    print(df)


    raise 'Final'


    """
    for i in STATES:
        # canditates = CANDIDATURA_PATH + "consulta_cand_" + YEAR + "_" + i + ".csv"
        votes = VOTACAO_ZONA_PATH + "votacao_candidato_munzona_" + YEAR + "_" + i + ".csv"

        print('Read votes: ' + votes)
        df0 = pd.read_csv(votes, sep=";", encoding = "ISO-8859-1")
        df0 = df0.replace(np.nan, '', regex=True)
        df0 = df0[['SQ_CANDIDATO', 'DS_CARGO', 'CD_CARGO', 'DS_SIT_TOT_TURNO', 'QT_VOTOS_NOMINAIS', 'NM_MUNICIPIO', 'DS_SIT_TOT_TURNO']]


        city = df0.groupby(['NM_MUNICIPIO'])

        data = []

        for name, group in city:
            print(name)

            df1 = group.query("CD_CARGO == 13 and NM_MUNICIPIO == '" + name + "'").sort_values(by=['QT_VOTOS_NOMINAIS'], inplace=False, ascending=False)

            sigma = df1['QT_VOTOS_NOMINAIS'].sum()

            elected = df1.query("DS_SIT_TOT_TURNO != 'SUPLENTE' and DS_SIT_TOT_TURNO != 'NÃO ELEITO' and DS_SIT_TOT_TURNO != '2º TURNO'")

            elected2 = elected.groupby(['SQ_CANDIDATO']).sum()
            df2 = elected2.sort_values(
                        by=['QT_VOTOS_NOMINAIS'],
                        inplace=False,
                        ascending=False)
            
            # Soma vereadores eleitos
            x = df2['QT_VOTOS_NOMINAIS'].count()
            print(x)
        
            q = (sigma / x)
            print(q)
            qq = np.ceil(q)

            data.append([YEAR, i, name, qq, x])

        final = pd.DataFrame(data, columns=['ANO_ELEICAO', 'SG_UF', 'NM_MUNICIPIO', 'Q_ELEITORAL', 'TOTAL_ELEITOS'])

        output = 'all.csv' # @TODO: 2014
        if os.path.isfile(output):
            final.to_csv(output, mode='a', index=False, sep=",", header=False)
        else:
            final.to_csv(output, index=False, sep=",")
    """
 




    """
    i = 'SP'
    votes = VOTACAO_ZONA_PATH + "votacao_candidato_munzona_" + YEAR + "_" + i + ".csv"

    df0 = pd.read_csv(votes, sep=";", encoding = "ISO-8859-1")
    df0 = df0.replace(np.nan, '', regex=True)
    df0 = df0[['SQ_CANDIDATO', 'DS_CARGO', 'CD_CARGO', 'DS_SIT_TOT_TURNO', 'QT_VOTOS_NOMINAIS', 'NM_MUNICIPIO', 'DS_SIT_TOT_TURNO']]

    sigma = group['QT_VOTOS_NOMINAIS'].sum()
    elected = group.query("DS_SIT_TOT_TURNO != 'SUPLENTE' and DS_SIT_TOT_TURNO != 'NÃO ELEITO'")
    print(elected)
    print(elected['CD_CARGO'].count())
    x = elected['CD_CARGO'].count()
    q = sigma / x
    print(q)
    """


if __name__ == "__main__":
    main()
