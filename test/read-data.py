#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os.path
import sys
import getopt


def main(argv):
    path = '/home/ecorbari/Downloads/votacao_candidato_munzona_2018/votacao_candidato_munzona_2018_BRASIL.csv'
    # df = pd.read_csv(path, sep=';', encoding='ISO-8859-1', low_memory=False, error_bad_lines=False, header=None)
    df = pd.read_csv(path, sep=';', encoding='ISO-8859-1', low_memory=False, error_bad_lines=False)
    print(df)

    filter = df["SG_UF"] == "MT"
    a = df.where(filter, inplace=False)
    b = a.groupby(['DS_CARGO']).count()
    print(b)


if __name__ == "__main__":
    main(sys.argv[1:])
