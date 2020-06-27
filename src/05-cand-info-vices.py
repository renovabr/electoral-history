#!/usr/bin/env python3

import pandas as pd
import sys
import getopt
from progress.bar import Bar
from config import mysql_user, mysql_password
from config import mysql_host, mysql_database, mysql_port
from sqlalchemy import create_engine
from utils import STATES, CAPITALS, COLS_VICES_XY, COLS_VICES_XY_NEW
from utils import CAND_TABLE_NAME, CAND_TABLE_NAME_ID
from utils import tic, toc, write_to_csv

DATABASE = 'mysql+mysqlconnector://' + mysql_user() + ':' + mysql_password() + \
    '@' + mysql_host() + ':' + mysql_port() + '/' + mysql_database()


def main(argv):
    global STATES
    year, state, ext, shift = (None, None, None, None)
    usage = '05-cand-info-vices.py -y 2016 -s SC -t 1 or 2 -e data.csv'

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
    else:
        shift = int(shift)

    engine = create_engine(DATABASE, echo=False)

    tic()

    for st in STATES:
        df = pd.read_sql("""SELECT nm_city FROM cand_info
            WHERE sg_uf = '{}' GROUP BY 1 ORDER BY 1""".format(st), engine)

        print(
            'Reading candidates for vice-mayor of all cities in the state of:',
            st,
            'shift:',
            shift)

        dfcount = df['nm_city'].count()
        bar = Bar('Progress', max=dfcount)

        for ct in df['nm_city'].tolist():
            if year == '2016' or year == '2012':
                df0 = pd.read_sql("""
                SELECT
                    t2.election_year,
                    t2.sg_uf,
                    t1.sq_candidate,
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
                    WHERE t1.election_year = '{}' AND t1.sg_uf = '{}'
                    AND t1.cd_position = 12 AND t2.nm_city = "{}" AND t1.nr_shift = '{}'
                    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23""".format(year, st, ct, shift), engine)

                df0 = df0.applymap(
                    lambda s: s.upper() if isinstance(
                        s, str) else s)

                df1 = pd.read_sql("""SELECT * FROM cand_info
                    WHERE sg_uf = '{}' AND nm_city = "{}"
                        AND ds_position = 'PREFEITO'""".format(st, ct), engine)

                df2 = pd.merge(df1, df0, on='sq_alliance', how='inner')
                df3 = df2[COLS_VICES_XY]

                df4 = df3.rename(columns=COLS_VICES_XY_NEW, inplace=False)
                df4 = df4.applymap(
                    lambda s: s.upper() if isinstance(
                        s, str) else s)

                if shift == 1:
                    if any(df4['ds_situ_tot_shift'] == '2º TURNO'):
                        df4 = df4.where(df4['ds_situ_tot_shift'] != '2º TURNO')
                    if any(df4['ds_situ_tot_shift'] == '#NULO#'):
                        df4.loc[df4['ds_situ_tot_shift'] == '#NULO#',
                                ['ds_situ_tot_shift']] = 'NÃO ELEITO'

                elif shift == 2:
                    if not df4.empty:
                        rank = df4['qt_votes_nominal_int'].nlargest(4).tolist()

                        for i in range(len(rank)):
                            if i == 0:
                                df4.loc[df4['qt_votes_nominal_int'] == rank[0], [
                                    'ds_situ_tot_shift']] = 'ELEITO'
                            if i == 1:
                                df4.loc[df4['qt_votes_nominal_int'] == rank[1], [
                                    'ds_situ_tot_shift']] = 'NÃO ELEITO'
                            if i == 2:
                                df4.loc[df4['qt_votes_nominal_int'] == rank[2], [
                                    'ds_situ_tot_shift']] = '2º TURNO'
                            if i == 3:
                                df4.loc[df4['qt_votes_nominal_int'] == rank[3], [
                                    'ds_situ_tot_shift']] = '2º TURNO'
                    else:
                        pass

                df5 = pd.read_sql("""SELECT * FROM cand_info
                    WHERE sg_uf = '{}' AND nm_city = "{}"
                        AND ds_position = 'VICE-PREFEITO'""".format(st, ct), engine)

                for i in df4['sq_candidate'].tolist():
                    if any(df5['sq_candidate'] == i):
                        df4 = df4[df4['sq_candidate'] != i]

                df6 = pd.read_sql("""
                SELECT
                    sq_candidate,
                    format(sum(amount_goods_declared), 0, 'de_DE') as amount_goods_declared,
                    sum(amount_goods_declared) as amount_goods_declared_float
                FROM raw_tse_cand_goods_declared
                    WHERE election_year = '{}' AND sg_uf = '{}' GROUP BY 1
                    ORDER BY 3 DESC""".format(year, st), engine)

                df7 = pd.merge(df4, df6, on='sq_candidate', how='inner')

                if df7.empty:
                    df4['amount_goods_declared'] = ''
                    df4['amount_goods_declared_float'] = 0
                    df7 = df4

                if not df7.empty:
                    final = df7.sort_values(
                        by=['qt_votes_nominal'],
                        inplace=False,
                        ascending=False)

                    if ext:
                        write_to_csv(final)

                    final.to_sql(
                        con=engine,
                        name=CAND_TABLE_NAME,
                        if_exists='append',
                        index=False,
                        index_label=CAND_TABLE_NAME_ID)
            else:
                raise ValueError('Invalid year')
            bar.next()
        bar.finish()

    toc()


if __name__ == "__main__":
    main(sys.argv[1:])
