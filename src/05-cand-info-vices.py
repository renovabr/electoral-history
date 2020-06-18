#!/usr/bin/env python3

import numpy as np
import pandas as pd
import datetime as dt
import os.path
import sys
import getopt
from progress.bar import Bar
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from utils import STATES, CAPITALS
from utils import tic, toc
from sqlalchemy import create_engine

DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()

TABLE_NAME = 'cand_info'
TABLE_NAME_ID = 'cand_info_id'

COLS_XY = [
    'election_year_x',
    'sg_uf_x',
    'sq_candidate_y',
    'nr_cpf_candidate_y',
    'nm_candidate_y',
    'sg_party_y',
    'nr_party_y',
    'nm_ballot_candidate_y',
    'ds_position_y',
    'ds_situ_tot_shift_y',
    'nm_city_x',
    'ds_situ_cand_y',
    'nm_email_y',
    'ds_genre_y',
    'ds_degree_instruction_y',
    'ds_race_color_y',
    'ds_occupation_y',
    'nr_campaign_max_expenditure_y',
    'st_reelection_y',
    'dt_birth_y',
    'nr_shift_y',
    'qt_votes_nominal',
    'qt_votes_nominal_int',
    'ds_election_y',
    'sq_alliance'
]

COLS_XY_NEW = {
    'election_year_x': 'election_year',
    'sg_uf_x': 'sg_uf',
    'sq_candidate_y': 'sq_candidate',
    'nr_cpf_candidate_y': 'nr_cpf_candidate',
    'nm_candidate_y': 'nm_candidate',
    'sg_party_y': 'sg_party',
    'nr_party_y': 'nr_party',
    'nm_ballot_candidate_y': 'nm_ballot_candidate',
    'ds_position_y': 'ds_position',
    'ds_situ_tot_shift_y': 'ds_situ_tot_shift',
    'nm_city_x': 'nm_city',
    'ds_situ_cand_y': 'ds_situ_cand',
    'nm_email_y': 'nm_email',
    'ds_genre_y': 'ds_genre',
    'ds_degree_instruction_y': 'ds_degree_instruction',
    'ds_race_color_y': 'ds_race_color',
    'ds_occupation_y': 'ds_occupation',
    'nr_campaign_max_expenditure_y': 'nr_campaign_max_expenditure',
    'st_reelection_y': 'st_reelection',
    'dt_birth_y': 'dt_birth',
    'nr_shift_y': 'nr_shift',
    'ds_election_y': 'ds_election'
}


def write_to_csv(df, output='data.csv'):
    if os.path.isfile(output):
        df.to_csv(output, mode='a', index=False, sep=",", header=False)
    else:
        df.to_csv(output, index=False, sep=",")


def main(argv):
    global STATES
    year, state, ext = (None, None, None)
    usage = '05-cand-info-vices.py -y 2016 -s SC -e data.csv'

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
        df = pd.read_sql("""SELECT nm_city FROM cand_info
            WHERE sg_uf = '{}' GROUP BY 1 ORDER BY 1""".format(st), engine)

        print('Reading candidates for vice-mayor of all cities in the state of:', st)

        dfcount = df['nm_city'].count()
        bar = Bar('Progress', max=dfcount)

        for ct in df['nm_city'].tolist():
            if year == '2016' or year == '2012':
                df0 = pd.read_sql("""
                SELECT
                    t2.election_year,
                    t2.sg_uf,
                    t1.sq_candidate ,
                    t1.nr_cpf_candidate,
                    t1.nm_candidate,
                    t1.sg_party,
                    t1.nr_party,
                    t1.nm_ballot_candidate,
                    t1.ds_position,
                    t1.ds_situ_tot_shift,
                    t2.nm_city,
                    t1.ds_situ_cand,
                    t1.nm_email,
                    t1.ds_genre,
                    t1.ds_degree_instruction,
                    t1.ds_race_color,
                    t1.ds_occupation,
                    t1.nr_campaign_max_expenditure,
                    t1.st_reelection,
                    t1.dt_birth,
                    t1.nr_shift,
                    t1.ds_election,
                    t1.sq_alliance
                FROM raw_tse_consult_candidates t1
                    INNER JOIN cand_info AS t2 ON (t1.sq_alliance = t2.sq_alliance)
                    WHERE t1.election_year = '{}' AND t1.sg_uf = '{}' AND t1.cd_position = 12 AND t2.nm_city = '{}'
                    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23""".format(year, st, ct), engine)

                df0 = df0.applymap(
                    lambda s: s.upper() if isinstance(
                        s, str) else s)

                df1 = pd.read_sql("""SELECT * FROM cand_info
                    WHERE sg_uf = '{}' AND nm_city = '{}'
                        AND ds_position = 'PREFEITO'""".format(st, ct), engine)

                df2 = pd.merge(df1, df0, on='sq_alliance', how='inner')

                df3 = df2[COLS_XY]

                df4 = df3.rename(columns=COLS_XY_NEW, inplace=False)
                df4 = df4.applymap(
                    lambda s: s.upper() if isinstance(
                        s, str) else s)
                df4 = df4.drop_duplicates()

                df5 = pd.read_sql("""SELECT * FROM cand_info
                    WHERE sg_uf = '{}' AND nm_city = '{}'
                        AND ds_position = 'VICE-PREFEITO'""".format(st, ct), engine)

                for i in df4['sq_candidate'].tolist():
                    if any(df5['sq_candidate'] == i):
                        df4 = df4[df4['sq_candidate'] != i]

                if not df4.empty:
                    final = df4.sort_values(
                        by=['qt_votes_nominal'],
                        inplace=False,
                        ascending=False)

                    if ext:
                        write_to_csv(final)

                    final.to_sql(
                        con=engine,
                        name=TABLE_NAME,
                        if_exists='append',
                        index=False,
                        index_label=TABLE_NAME_ID)
            else:
                raise ValueError('Invalid year')
            bar.next()
        bar.finish()

    toc()


if __name__ == "__main__":
    main(sys.argv[1:])
