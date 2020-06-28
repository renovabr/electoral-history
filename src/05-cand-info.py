#!/usr/bin/env python3

import pandas as pd
import sys
import getopt
from progress.bar import Bar
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from sqlalchemy import create_engine
from utils import STATES, CAPITALS
from utils import CAND_TABLE_NAME, CAND_TABLE_NAME_ID
from utils import tic, toc, write_to_csv

DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()


def main(argv):
    global STATES
    year, state, ext, shift = (None, None, None, None)
    usage = '05-cand-info.py -y 2016 -s SC -t 1 or 2 -e data.csv'

    try:
        opts, _args = getopt.getopt(
            argv, 'hy:s:t:e:', ['year=', 'state=', 'shift=', 'ext='])
    except getopt.GetoptError:
        print(usage)
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ('-y', '--year'):
            year = arg
        elif opt in ('-s', '--state'):
            state = arg
        elif opt in ('-t', '--shift'):
            shift = arg
        elif opt in ('-e', '--ext='):
            ext = arg

    if year == '2010' or year == '2012' or year == '2014' or year == '2016' or year == '2018':
        if year == '2016' or year == '2012':
            STATES.remove('DF')
    else:
        print('Year is invalid!')
        print(usage)
        sys.exit()

    if state:
        STATES = list(filter(lambda x: x == str(state), STATES))

    if not shift:
        print('The shift number is required! 1 or 2 shift.')
        sys.exit()

    engine = create_engine(DATABASE, echo=False)

    tic()

    for st in STATES:
        print(
            'Reading candidates (%s) for the state: %s in shift: %s' %
            (year, st, shift))

        bar = Bar('Progress', max=100)

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

        bar.next(25)

        df0 = df0.applymap(lambda s: s.upper() if isinstance(s, str) else s)
        df1 = pd.DataFrame()

        if year == '2016' or year == '2012':
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
                ORDER BY sum(qt_votes_nominal) DESC""".format(year, st, shift), engine)
        else:
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
                ORDER BY sum(qt_votes_nominal) DESC""".format(year, st, shift), engine)
            df1['nm_city'] = CAPITALS[st]

        bar.next(25)
        df1 = df1.applymap(lambda s: s.upper() if isinstance(s, str) else s)

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

        bar.next(25)
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
            write_to_csv(final)

        bar.next(25)

        final.to_sql(
            con=engine,
            name=CAND_TABLE_NAME,
            if_exists='append',
            index=False,
            index_label=CAND_TABLE_NAME_ID)

        bar.finish()

    toc()


if __name__ == "__main__":
    main(sys.argv[1:])
