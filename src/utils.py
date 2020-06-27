import time
import pandas as pd
from config import mysql_host, mysql_database, mysql_port
from config import mysql_user, mysql_password, mysql_raise_on_warnings

DATABASE = {
    'host': mysql_host(),
    'database': mysql_database(),
    'port': mysql_port(),
    'user': mysql_user(),
    'password': mysql_password(),
    'raise_on_warnings': mysql_raise_on_warnings()
}

CAND_TABLE_NAME = 'cand_info'
CAND_TABLE_NAME_ID = 'cand_info_id'

TIC_TIME_START = 0

STATES = [
    'AC',
    'AL',
    'AP',
    'AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MT',
    'MS',
    'MG',
    'PA',
    'PB',
    'PR',
    'PE',
    'PI',
    'RJ',
    'RN',
    'RS',
    'RO',
    'RR',
    'SC',
    'SP',
    'SE',
    'TO'
]

CAPITALS = {
    'AC': 'RIO BRANCO',
    'AL': 'MACEIÓ',
    'AP': 'MACAPÁ',
    'AM': 'MANAUS',
    'BA': 'SALVADOR',
    'CE': 'FORTALEZA',
    'DF': 'BRASÍLIA',
    'ES': 'VITÓRIA',
    'GO': 'GOIÂNIA',
    'MA': 'SÃO LUÍS',
    'MT': 'CUIABÁ',
    'MS': 'CAMPO GRANDE',
    'MG': 'BELO HORIZONTE',
    'PA': 'BELÉM',
    'PB': 'JOÃO PESSOA',
    'PR': 'CURITIBA',
    'PE': 'RECIFE',
    'PI': 'TERESINA',
    'RJ': 'RIO DE JANEIRO',
    'RN': 'NATAL',
    'RS': 'PORTO ALEGRE',
    'RO': 'PORTO VELHO	',
    'RR': 'BOA VISTA',
    'SC': 'FLORIANÓPOLIS',
    'SP': 'SÃO PAULO',
    'SE': 'ARACAJU',
    'TO': 'PALMAS'
}

COLS_CONSULT_CANDIDATES_2010 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'nr_shift',
    'ds_election',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'cd_position',
    'ds_position',
    'nm_candidate',
    'sq_candidate',
    'nr_candidate',
    'nr_cpf_candidate',
    'nm_ballot_candidate',
    'cd_situ_cand',
    'ds_situ_cand',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'rm_col_2',
    'ds_comp_alliance',
    'nm_alliance',
    'cd_occupation',
    'ds_occupation',
    'dt_birth',
    'nr_doc_electoral_cand',
    'nr_age_date_inauguration',
    'cd_genre',
    'ds_genre',
    'cd_degree_instruction',
    'ds_degree_instruction',
    'cd_marital_status',
    'ds_marital_status',
    'cd_nationality',
    'ds_nationality',
    'sg_uf_birth',
    'cd_city_birth',
    'nm_city_birth',
    'nr_campaign_max_expenditure',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift'
]

COLS_CONSULT_CANDIDATES_2012 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'nr_shift',
    'ds_election',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'cd_position',
    'ds_position',
    'nm_candidate',
    'sq_candidate',
    'nr_candidate',
    'nr_cpf_candidate',
    'nm_ballot_candidate',
    'cd_situ_cand',
    'ds_situ_cand',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'rm_col_2',
    'ds_comp_alliance',
    'nm_alliance',
    'cd_occupation',
    'ds_occupation',
    'dt_birth',
    'nr_doc_electoral_cand',
    'nr_age_date_inauguration',
    'cd_genre',
    'ds_genre',
    'cd_degree_instruction',
    'ds_degree_instruction',
    'cd_marital_status',
    'ds_marital_status',
    'cd_nationality',
    'ds_nationality',
    'sg_uf_birth',
    'cd_city_birth',
    'nm_city_birth',
    'nr_campaign_max_expenditure',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift',
    'nm_email'
]

COLS_CONSULT_CANDIDATES = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'type_election',
    'nm_type_election',
    'nr_shift',
    'cd_election',
    'ds_election',
    'dt_election',
    'tp_coverage',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'cd_position',
    'ds_position',
    'sq_candidate',
    'nr_candidate',
    'nm_candidate',
    'nm_ballot_candidate',
    'nm_social_candidate',
    'nr_cpf_candidate',
    'nm_email',
    'cd_situ_cand',
    'ds_situ_cand',
    'cd_detail_situ_cand',
    'ds_detail_situ_cand',
    'tp_association',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'nm_alliance',
    'ds_comp_alliance',
    'cd_nationality',
    'ds_nationality',
    'sg_uf_birth',
    'cd_city_birth',
    'nm_city_birth',
    'dt_birth',
    'nr_age_date_inauguration',
    'nr_doc_electoral_cand',
    'cd_genre',
    'ds_genre',
    'cd_degree_instruction',
    'ds_degree_instruction',
    'cd_marital_status',
    'ds_marital_status',
    'cd_race_color',
    'ds_race_color',
    'cd_occupation',
    'ds_occupation',
    'nr_campaign_max_expenditure',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift',
    'st_reelection',
    'st_declare_goods',
    'nr_protocol_cand',
    'nr_process'
]

COLS_VOTES_CANDIDATES_2010 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'nr_shift',
    'ds_election',
    'sg_uf',
    'sg_ue',
    'cd_city',
    'nm_city',
    'nr_zone',
    'cd_position',
    'nr_candidate',
    'sq_candidate',
    'nm_candidate',
    'nm_ballot_candidate',
    'ds_position',
    'cd_situ_cand',
    'ds_situ_cand',
    'cd_detail_situ_cand',
    'ds_detail_situ_cand',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'nm_alliance',
    'rm_col_2',
    'qt_votes_nominal'
]

COLS_VOTES_CANDIDATES_2012 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'nr_shift',
    'ds_election',
    'sg_uf',
    'sg_ue',
    'cd_city',
    'nm_city',
    'nr_zone',
    'cd_position',
    'nr_candidate',
    'sq_candidate',
    'nm_candidate',
    'nm_ballot_candidate',
    'ds_position',
    'cd_situ_cand',
    'ds_situ_cand',
    'cd_detail_situ_cand',
    'ds_detail_situ_cand',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'nm_alliance',
    'ds_comp_alliance',
    'qt_votes_nominal'
]

COLS_VOTES_CANDIDATES = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'type_election',
    'nm_type_election',
    'nr_shift',
    'cd_election',
    'ds_election',
    'dt_election',
    'tp_coverage',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'cd_city',
    'nm_city',
    'nr_zone',
    'cd_position',
    'ds_position',
    'sq_candidate',
    'nr_candidate',
    'nm_candidate',
    'nm_ballot_candidate',
    'nm_social_candidate',
    'cd_situ_cand',
    'ds_situ_cand',
    'cd_detail_situ_cand',
    'ds_detail_situ_cand',
    'tp_association',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'nm_alliance',
    'ds_comp_alliance',
    'cd_situ_tot_shift',
    'ds_situ_tot_shift',
    'st_vote_in_transit',
    'qt_votes_nominal'
]

COLS_VOTES_PARTIES_2010_2012 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'type_election',
    'nm_type_election',
    'sg_uf',
    'sg_ue',
    'cd_city',
    'nm_city',
    'nr_zone',
    'cd_position',
    'ds_position',
    'tp_coverage',
    'nm_alliance',
    'ds_comp_alliance',
    'sg_party',
    'nr_party',
    'nm_party',
    'qt_votes_nominal',
    'qt_votes_legend',
    'sq_alliance'
]

COLS_VOTES_PARTIES = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'type_election',
    'nm_type_election',
    'nr_shift',
    'cd_election',
    'ds_election',
    'dt_election',
    'tp_coverage',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'cd_city',
    'nm_city',
    'nr_zone',
    'cd_position',
    'ds_position',
    'tp_association',
    'nr_party',
    'sg_party',
    'nm_party',
    'sq_alliance',
    'nm_alliance',
    'ds_comp_alliance',
    'st_vote_in_transit',
    'qt_votes_nominal',
    'qt_votes_legend'
]


COLS_GOODS_DECLARED_2010_2012 = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'nm_type_election',
    'sg_uf',
    'sq_candidate',
    'cd_type_cand_goods_declared',
    'ds_type_cand_goods_declared',
    'ds_cand_goods_declared',
    'amount_goods_declared',
    'dt_tse_last_update',
    'hh_tse_last_update'
]

COLS_GOODS_DECLARED = [
    'dt_tse_generation',
    'hh_tse_generation',
    'election_year',
    'type_election',
    'nm_type_election',
    'cd_election',
    'ds_election',
    'dt_election',
    'sg_uf',
    'sg_ue',
    'nm_ue',
    'sq_candidate',
    'nr_order_candidate',
    'cd_type_cand_goods_declared',
    'ds_type_cand_goods_declared',
    'ds_cand_goods_declared',
    'amount_goods_declared',
    'dt_tse_last_update',
    'hh_tse_last_update'
]

COLS_VICES_XY = [
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

COLS_VICES_XY_NEW = {
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


def standardize_df_cand(df, year):
    df['type_election'] = 0
    df['nm_type_election'] = ''
    df['cd_election'] = 0
    df['dt_election'] = '01/01/' + str(year)
    df['tp_coverage'] = df['ds_election']
    df['nm_social_candidate'] = ''
    df['cd_detail_situ_cand'] = 0
    df['ds_detail_situ_cand'] = ''
    df['tp_association'] = ''
    df['cd_race_color'] = 0
    df['ds_race_color'] = ''
    df['st_reelection'] = ''
    df['st_declare_goods'] = ''
    df['nr_protocol_cand'] = ''
    df['nr_process'] = ''

    if year == 2010:
        df['nm_email'] = ''
    df = df.drop(columns=['rm_col_2'], axis=1)

    df = df[[
        'dt_tse_generation',
        'hh_tse_generation',
        'election_year',
        'type_election',
        'nm_type_election',
        'nr_shift',
        'cd_election',
        'ds_election',
        'dt_election',
        'tp_coverage',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'cd_position',
        'ds_position',
        'sq_candidate',
        'nr_candidate',
        'nm_candidate',
        'nm_ballot_candidate',
        'nm_social_candidate',
        'nr_cpf_candidate',
        'nm_email',
        'cd_situ_cand',
        'ds_situ_cand',
        'cd_detail_situ_cand',
        'ds_detail_situ_cand',
        'tp_association',
        'nr_party',
        'sg_party',
        'nm_party',
        'sq_alliance',
        'nm_alliance',
        'ds_comp_alliance',
        'cd_nationality',
        'ds_nationality',
        'sg_uf_birth',
        'cd_city_birth',
        'nm_city_birth',
        'dt_birth',
        'nr_age_date_inauguration',
        'nr_doc_electoral_cand',
        'cd_genre',
        'ds_genre',
        'cd_degree_instruction',
        'ds_degree_instruction',
        'cd_marital_status',
        'ds_marital_status',
        'cd_race_color',
        'ds_race_color',
        'cd_occupation',
        'ds_occupation',
        'nr_campaign_max_expenditure',
        'cd_situ_tot_shift',
        'ds_situ_tot_shift',
        'st_reelection',
        'st_declare_goods',
        'nr_protocol_cand',
        'nr_process'
    ]]
    return df


def standardize_df_votes_cand(df, year):
    df['type_election'] = 0
    df['nm_type_election'] = ''
    df['cd_election'] = 0
    df['dt_election'] = '01/01/' + str(year)
    df['tp_coverage'] = df['ds_election']
    df['nm_ue'] = ''
    df['nm_social_candidate'] = ''
    df['tp_association'] = ''
    df['ds_comp_alliance'] = ''
    df['st_vote_in_transit'] = ''

    if year == 2010:
        df = df.drop(columns=['rm_col_2'], axis=1)

    df = df[[
        'dt_tse_generation',
        'hh_tse_generation',
        'election_year',
        'type_election',
        'nm_type_election',
        'nr_shift',
        'cd_election',
        'ds_election',
        'dt_election',
        'tp_coverage',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'cd_city',
        'nm_city',
        'nr_zone',
        'cd_position',
        'ds_position',
        'sq_candidate',
        'nr_candidate',
        'nm_candidate',
        'nm_ballot_candidate',
        'nm_social_candidate',
        'cd_situ_cand',
        'ds_situ_cand',
        'cd_detail_situ_cand',
        'ds_detail_situ_cand',
        'tp_association',
        'nr_party',
        'sg_party',
        'nm_party',
        'sq_alliance',
        'nm_alliance',
        'ds_comp_alliance',
        'cd_situ_tot_shift',
        'ds_situ_tot_shift',
        'st_vote_in_transit',
        'qt_votes_nominal'
    ]]

    return df


def standardize_df_votes_party(df, year):
    df['nr_shift'] = 0
    df['cd_election'] = 0
    df['dt_election'] = '01/01/' + str(year)
    df['nm_ue'] = ''
    df['tp_association'] = ''
    df['st_vote_in_transit'] = ''
    df['ds_election'] = ''

    df = df[[
        'dt_tse_generation',
        'hh_tse_generation',
        'election_year',
        'type_election',
        'nm_type_election',
        'nr_shift',
        'cd_election',
        'ds_election',
        'dt_election',
        'tp_coverage',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'cd_city',
        'nm_city',
        'nr_zone',
        'cd_position',
        'ds_position',
        'tp_association',
        'nr_party',
        'sg_party',
        'nm_party',
        'sq_alliance',
        'nm_alliance',
        'ds_comp_alliance',
        'st_vote_in_transit',
        'qt_votes_nominal',
        'qt_votes_legend'
    ]]

    return df


def standardize_df_goods_declared(df, year):
    df['type_election'] = 0
    df['cd_election'] = 0
    df['ds_election'] = ''
    df['dt_election'] = '01/01/' + str(year)
    df['sg_ue'] = ''
    df['nm_ue'] = ''
    df['nr_order_candidate'] = 0

    df = df[[
        'dt_tse_generation',
        'hh_tse_generation',
        'election_year',
        'type_election',
        'nm_type_election',
        'cd_election',
        'ds_election',
        'dt_election',
        'sg_uf',
        'sg_ue',
        'nm_ue',
        'sq_candidate',
        'nr_order_candidate',
        'cd_type_cand_goods_declared',
        'ds_type_cand_goods_declared',
        'ds_cand_goods_declared',
        'amount_goods_declared',
        'dt_tse_last_update',
        'hh_tse_last_update'
    ]]

    return df


def tic():
    TIC_TIME_START = time.time()
    print('%s\n' % TIC_TIME_START)


def toc():
    end = time.time()
    temp = end - TIC_TIME_START
    hours = temp // 3600
    temp = temp - 3600 * hours
    minutes = temp // 60
    seconds = temp - 60 * minutes
    print('\n%d:%d:%d' % (hours, minutes, seconds))


def write_to_csv(df, output='data.csv'):
    import os.path
    if os.path.isfile(output):
        df.to_csv(output, mode='a', index=False, sep=",", header=False)
    else:
        df.to_csv(output, index=False, sep=",")
