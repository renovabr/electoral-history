#!/usr/bin/env python3

import numpy as np
import pandas as pd
import datetime as dt
import os.path
import sys
import getopt
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from utils import STATES
from utils import tic, toc
from sqlalchemy import create_engine

DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()


def main(argv):
    global STATES
    year, state = (None, None)
    usage = '04-anl-compute-votes.py -y 2014 -s SC'

    try:
        opts, _args = getopt.getopt(
            argv, 'hy:s:', ['year=', 'state='])
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
        df0 = pd.read_sql("""SELECT
          election_year,
          sg_uf,
          sq_candidate,
          nr_cpf_candidate,
          nm_candidate,
          sg_party
          FROM raw_tse_consult_candidates
          WHERE election_year = '{}' AND
          sg_uf = '{}'""".format(year, st), engine)

        print(df0)

        print('Read votes: ' + st)
        df1 = pd.read_sql("""SELECT
          sq_candidate,
          nm_ballot_candidate,
          ds_position,
          ds_situ_tot_shift,
          format(sum(qt_votes_nominal), 0, 'de_DE') AS qt_votes_nominal
          FROM raw_tse_voting_cand_city
          WHERE
          election_year = '{}'
          AND sg_uf = '{}'
          AND nr_shift = 1
          GROUP BY 1, 2, 3, 4
          ORDER BY sum(qt_votes_nominal) DESC""".format(year, st), engine)

        print(df1)

        # df2 = df1.groupby(['sq_candidate']).sum()
        df3 = pd.merge(df0, df1, on='sq_candidate', how='inner')
        df3 = df3.drop_duplicates()

        df3['created_at'] = dt.datetime.now()
        df3['updated_at'] = dt.datetime.now()
        final = df3.sort_values(
            by=['qt_votes_nominal'],
            inplace=False,
            ascending=False)

        # final.to_csv('test.csv', index=False, sep=",")
        print('Inserting the data in table: votes_computed')
        final.to_sql('votes_computed', con=engine, if_exists='append',
                     index_label='votes_computed_id', chunksize=1000)

    toc()


if __name__ == "__main__":
    main(sys.argv[1:])
