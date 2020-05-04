#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os.path
import sys
import getopt
import mysql.connector
from progress.bar import Bar
from utils import *


def main(argv):
    global STATES
    year, path, ext, state = (None, None, None, None)
    usage = '02-votacao-candidato-munzona.py -y 2014 -p /tmp/tse/2014/ -e csv or txt'

    try:
        opts, args = getopt.getopt(
            argv, 'hy:p:e:s:', [
                'year=', 'path=', 'ext=', 'state='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ('-y', '--year'):
            year = arg
        elif opt in ('-p', '--path'):
            path = arg
        elif opt in ('-e', '--ext'):
            ext = arg
        elif opt in ('-s', '--state'):
            state = arg

    if year == '2010' or year == '2012' or year == '2014' or year == '2016' or year == '2018':
        if year == '2012' or year == '2016':
            STATES.remove('DF')
    else:
        print('Year is invalid!')
        sys.exit()

    if not os.path.isdir(path):
        print('Directory is invalid!')
        sys.exit()

    if ext == 'csv' or ext == 'txt':
        pass
    else:
        print('Extension is invalid!')
        sys.exit()

    if state:
        STATES = list(filter(lambda x: x == str(state), STATES))

    cnx = mysql.connector.connect(**DATABASE)
    cur = cnx.cursor(buffered=True)
    dfcount = 0

    for st in STATES:
        votes = path + 'votacao_candidato_munzona_' + year + '_' + st + '.' + ext

        if not os.path.isfile(votes):
            print(votes)
            raise 'File or path not exist...'

        print('Inserting data (%s) in the state: %s' % (year, st))
        if year == '2010':
            df0 = pd.read_csv(
                votes,
                sep=';',
                encoding='ISO-8859-1',
                low_memory=False,
                error_bad_lines=False,
                header=None)
            df1 = df0.set_axis(
                COLS_VOTES_CANDIDATES_2010,
                axis=1,
                inplace=False)
            df1 = standardize_df_votes_cand(df1, int(year))
        elif year == '2012':
            df0 = pd.read_csv(
                votes,
                sep=';',
                encoding='ISO-8859-1',
                low_memory=False,
                error_bad_lines=False,
                header=None)
            df1 = df0.set_axis(
                COLS_VOTES_CANDIDATES_2012,
                axis=1,
                inplace=False)
            df1 = standardize_df_votes_cand(df1, int(year))
        else:
            df1 = pd.read_csv(
                votes,
                sep=';',
                encoding='ISO-8859-1',
                low_memory=False,
                error_bad_lines=False)

        df1 = df1.set_axis(COLS_VOTES_CANDIDATES, axis=1, inplace=False)
        df1 = df1.replace(np.nan, '', regex=True)
        dfcount = df1['election_year'].count()

        df1['dt_tse_generation'] = pd.to_datetime(
            df1['dt_tse_generation']).astype('str')
        df1['hh_tse_generation'] = pd.to_datetime(
            df1['hh_tse_generation'], format='%H:%M:%S').dt.time
        df1['dt_election'] = pd.to_datetime(df1['dt_election']).astype('str')

        df1['election_year'] = df1['election_year'].astype('str')
        df1['end_partition'] = year + '-01-01 00:00:00'

        cols = ','.join([str(i) for i in df1.columns.tolist()])
        bar = Bar('Progress', max=dfcount)

        for i, r in df1.iterrows():
            sql = 'INSERT INTO raw_tse_voting_cand_city (' + \
                cols + ') VALUES (' + '%s,' * (len(r) - 1) + '%s)'
            cur.execute(sql, tuple(r))
            bar.next()
        cnx.commit()
        bar.finish()

    cur.close()
    cnx.close()


if __name__ == "__main__":
    main(sys.argv[1:])
