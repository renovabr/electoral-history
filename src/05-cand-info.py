#!/usr/bin/env python3

import numpy as np
import pandas as pd
import datetime as dt
import os.path
import sys
import getopt
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from utils import STATES, CAPITALS
from utils import tic, toc
from sqlalchemy import create_engine

DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()

TABLE_NAME = 'cand_info'
TABLE_NAME_ID = 'cand_info_id'


def write_to_csv(df, output='data.csv'):
    if os.path.isfile(output):
        df.to_csv(output, mode='a', index=False, sep=",", header=False)
    else:
        df.to_csv(output, index=False, sep=",")


def main(argv):
    global STATES
    year, state, ext = (None, None, None)
    usage = '04-cand-info.py -y 2016 -s SC -e data.csv'

    try:
        opts, _args = getopt.getopt(
            argv, 'hy:s:e:', ['year=', 'state=', 'ext='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ('-y', '--year'):
            year = arg
        elif opt in ('-s', '--state'):
            state = arg
        elif opt in ('-e', '--ext='):
            ext = arg

    if year == '2010' or year == '2012' or year == '2014' or year == '2016' or year == '2018':
        if year == '2016' or year == '2012':
            STATES.remove('DF')
    else:
        print('Year is invalid!')
        sys.exit()

    if state:
        STATES = list(filter(lambda x: x == str(state), STATES))

    engine = create_engine(DATABASE, echo=False)

    tic()

    for st in STATES:
        print('Read canditates: ' + st)

        df0 = pd.read_sql("""
          SELECT
            election_year,
            sg_uf,
            sq_candidate,
            nr_cpf_candidate,
            nm_candidate,
            sg_party,
            nr_party,
            nm_email,
            ds_genre,
            ds_degree_instruction,
            ds_race_color,
            ds_occupation,
            nr_campaign_max_expenditure,
            st_reelection,
            dt_birth,
            nr_shift,
            ds_election,
            sq_alliance
          FROM raw_tse_consult_candidates
            WHERE election_year = '{}' AND sg_uf = '{}'""".format(year, st), engine)

        df0 = df0.applymap(lambda s: s.upper() if isinstance(s, str) else s)

        df = pd.read_sql("""SELECT nr_shift FROM raw_tse_voting_cand_city
            WHERE sg_uf = '{}' GROUP BY 1""".format(st), engine)

        for shitf in df['nr_shift'].tolist():
            print('Shift number: ' + str(shitf))
            df1 = 0

            if year == '2016' or year == '2012':
                print('Regional election')
                df1 = pd.read_sql("""
                SELECT
                    sq_candidate,
                    nm_ballot_candidate,
                    ds_position,
                    ds_situ_tot_shift,
                    nm_city,
                    ds_situ_cand,
                    format(sum(qt_votes_nominal), 0, 'de_DE') as qt_votes_nominal,
                    sum(qt_votes_nominal) AS qt_votes_nominal_int
                FROM raw_tse_voting_cand_city
                    WHERE election_year = '{}' AND sg_uf = '{}' AND nr_shift = '{}'
                    GROUP BY 1, 2, 3, 4, 5, 6
                    ORDER BY sum(qt_votes_nominal) DESC""".format(year, st, shitf), engine)
            else:
                print('National and state election')
                df1 = pd.read_sql("""
                SELECT
                    sq_candidate,
                    nm_ballot_candidate,
                    ds_position,
                    ds_situ_tot_shift,
                    ds_situ_cand,
                    format(sum(qt_votes_nominal), 0, 'de_DE') as qt_votes_nominal,
                    sum(qt_votes_nominal) AS qt_votes_nominal_int
                FROM raw_tse_voting_cand_city
                    WHERE election_year = '{}' AND sg_uf = '{}' AND nr_shift = '{}'
                    GROUP BY 1, 2, 3, 4, 5
                    ORDER BY sum(qt_votes_nominal) DESC""".format(year, st, shitf), engine)
                df1['nm_city'] = CAPITALS[st]

            df1 = df1.applymap(
                lambda s: s.upper() if isinstance(
                    s, str) else s)

            df2 = pd.merge(df0, df1, on='sq_candidate', how='inner')
            df3 = df2.drop_duplicates(['sq_candidate'], keep='last')

            df4 = pd.read_sql("""
            SELECT
                sq_candidate,
                format(sum(amount_goods_declared), 0, 'de_DE') as amount_goods_declared,
                sum(amount_goods_declared) as amount_goods_declared_float
            FROM raw_tse_cand_goods_declared
                WHERE election_year = '{}' AND sg_uf = '{}' GROUP BY 1
                ORDER BY 3 DESC""".format(year, st), engine)

            df5 = pd.merge(df3, df4, on='sq_candidate', how='inner')

            if df5.empty:
                df3['amount_goods_declared'] = ''
                df3['amount_goods_declared_float'] = 0
                df5 = df3

            final = df5.sort_values(
                by=['qt_votes_nominal'],
                inplace=False,
                ascending=False)

            if ext:
                print('Write/append data in CSV file:', ext)
                write_to_csv(final)

            print('Inserting the data in table:', TABLE_NAME)
            final.to_sql(
                con=engine,
                name=TABLE_NAME,
                if_exists='append',
                index=False,
                index_label=TABLE_NAME_ID)

    toc()


if __name__ == "__main__":
    main(sys.argv[1:])
