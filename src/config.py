import configparser

config = configparser.ConfigParser()
config.read('../config.ini')


def mysql_host():
    return config['mysql']['host']


def mysql_database():
    return config['mysql']['database']


def mysql_port():
    return config['mysql']['port']


def mysql_user():
    return config['mysql']['user']


def mysql_password():
    return config['mysql']['password']


def mysql_raise_on_warnings():
    return config['mysql'].getboolean('raise_on_warnings')
