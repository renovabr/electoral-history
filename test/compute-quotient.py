#!/usr/bin/env python3

import sys
sys.path.append('../src')
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import os.path


DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()
YEAR = '2016'


def main():
    engine = create_engine(DATABASE, echo=False)

    print('Read states. Wait...')
    states = pd.read_sql(
        """SELECT sg_uf AS STATES FROM raw_tse_voting_cand_city WHERE election_year = '{}' GROUP BY 1""".format(YEAR),
        engine)
        
    output = 'result-quotient-' + YEAR + '.csv'

    for st in states['STATES'].to_list():
        print('Read votes: ' + st)

        df0 = pd.read_sql("""
          SELECT
            sq_candidate AS SQ_CANDIDATO,
            ds_position AS DS_CARGO,
            cd_position AS CD_CARGO,
            ds_situ_tot_shift AS DS_SIT_TOT_TURNO,
            qt_votes_nominal AS QT_VOTOS_NOMINAIS,
            nm_city AS NM_MUNICIPIO
          FROM
            raw_tse_voting_cand_city
          WHERE
            election_year = '{}'
            AND sg_uf = '{}'""".format(YEAR, st), engine)

        city = df0.groupby(['NM_MUNICIPIO'])
        data = []

        for name, group in city:
            df1 = group.query(
                "CD_CARGO == 13 and NM_MUNICIPIO == '" +
                name +
                "'").sort_values(
                by=['QT_VOTOS_NOMINAIS'],
                inplace=False,
                ascending=False)

            sigma1 = df1['QT_VOTOS_NOMINAIS'].sum()
            elected = df1.query(
                "DS_SIT_TOT_TURNO != 'SUPLENTE' and DS_SIT_TOT_TURNO != 'NÃO ELEITO' and DS_SIT_TOT_TURNO != '2º TURNO'")

            sigma2 = elected.groupby(['SQ_CANDIDATO']).sum()
            sigma2 = sigma2['QT_VOTOS_NOMINAIS'].count()

            x = (sigma1 / sigma2)
            q = np.ceil(x)

            data.append([YEAR, st, name, q, sigma2])

        df = pd.DataFrame(
            data,
            columns=[
                'ANO_ELEICAO',
                'SG_UF',
                'NM_MUNICIPIO',
                'Q_ELEITORAL',
                'TOTAL_ELEITOS'])

        if os.path.isfile(output):
            df.to_csv(output, mode='a', index=False, sep=",", header=False)
        else:
            df.to_csv(output, index=False, sep=",")


if __name__ == "__main__":
    main()
