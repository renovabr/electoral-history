<img src="doc/img/brazil-vector.png" align="right" width="180" height="180"/>

# Brazilian Electoral History

<p align="center"> 
<a href="https://www.renovabr.org">
<img border="0" alt="RenovaBR Foundation" src="https://raw.githubusercontent.com/renovabr/electoral-history/master/doc/img/renovabr.png">
</a>
</p>

[ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) project that collects data from the **Brazilian Electoral Data Repository** and imports it into a **MySQL** database. Electoral years available: *2010, 2012, 2014, 2016, 2018*. The full import of every year totals **23.271.685** million lines in the database.

## Synopsis

This is a raw data processing ([ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load)) project for standardizing information for a MySQL Database. The Brazilian Electoral History data is made available by **TSE** on the website [TSE Electoral Data Repository](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais).

The process of importing the data into an SQL database aims to facilitate the development of other systems as well as for statistical analysis.

### Architecture

This project uses the following technologies:

  * Python
  * MySQL

<p align="center"> 
<img src="https://raw.githubusercontent.com/renovabr/electoral-history/master/doc/img/python-mysql.png">
</p>

Three tables are created in the database called (*electoral_history*) to store the data. Are they:

| Table  | Description | 
| ------ | ----------------------------------------------------  | 
| raw_tse_consult_candidates | Contains all candidates.          |
| raw_tse_voting_cand_city   | Contains candidate votes by city. |
| raw_tse_voting_party_city  | Contains party votes by city.     |

>Note: All tables are partitioned by the election year.

### Requeriments

You must have it installed on your workstation:

  * [MySQL 8 or higher](https://www.mysql.com/downloads/)
  * [Python 3 or higher](https://www.python.org/downloads/)
  * [Virtualenv](https://pypi.org/project/virtualenv/)
  
And preferably use a **GNU Linux** distribution.

#### 1. Get the code and data

Now run the commands below to compile the project:

```shell
$ git clone https://github.com/renovabr/electoral-history.git
$ cd electoral-history
```

Enter **pipenv** at the root of the *electoral-history* folder for the tests:

```shell
$ pipenv shell
$ pipenv install
```

The **tse-data.sh** script downloads the raw data using the year as a parameter. Example to download the year 2010:

```shell
$ ./tse-data.sh 2010
```

You can also download them all using the command:

```shell
$ for i in "2010" "2012" "2014" "2016" "2018"; do ./tse-data.sh ${i}; done
```

Wait for the data to download! The data is downloaded in the project folder at: *data/tse/YEAR*

#### 2. Set MySQL database 

Access the database with user **root** check if everything is working.

```shell
$ mysql -u root -p
```

Then run the *sql/schema.sql* that is within the project.

```shell
$ mysql -u root -p < sql/schema.sql
```

A database will be created called: *electoral_historal* with three tables and a user with access to a database called *winston*. The database connection settings can be changed in the *src/utils.py* file.

#### 3. Import all data to MySQL 

To import the candidates data for all years, use the script: **run-import-all.sh**.

```shell
$ ./run-import-all.sh 'consulta-cand'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./01-consulta-cand.py -y 2010 -s 'SP' \
  -p ../data/tse/2010/consulta_cand_2010/ -e txt
```

The same procedure applies to the other tables. To import all candidates voting data, use the command:

```shell
$ ./run-import-all.sh 'votacao-candidato'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./02-votacao-candidato-munzona.py -y 2010 -s 'SP' -p \
  ../data/tse/2010/votacao_candidato_munzona_2010/ -e txt
```

For the import of votes by party:

```shell
$ ./run-import-all.sh 'votacao-partido'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./03-votacao-partido-munzona.py -y 2010 -s SC \
  -p ../data/tse/2010/votacao_partido_munzona_2010/ -e txt
```

#### 3.Checking and analyzing data 

There is a data dictionary that can be downloaded here: [Dictionary](doc/dictionary-data.xlsx). 

Checking positions in the *2016* election:

```sql
SELECT
  ds_position 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2016' 
GROUP BY
  1 
ORDER BY
  1;
```

| Result   |
| -------- | 
| Prefeito |
| Vereador |

Checking positions in the *2018* election:

```sql
SELECT
  ds_position 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
GROUP BY
  1 
ORDER BY
  1;
```

| Result   |
| -------- | 
| Deputado Distrital |
| Deputado Estadual  |
| Deputado Federal   |
| Governador         |
| Senador            |

```sql
SELECT
  sq_candidate AS sq,
  nm_ballot_candidate AS name,
  ds_position AS position,
  nm_city AS city,
  sum(qt_votes_nominal) AS votes 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
  AND sg_uf = 'SC' 
  AND cd_city = 81051 
  AND cd_position = 3 
GROUP BY
  1,
  2,
  3,
  4 
ORDER BY
  5 DESC;
```

| SQ           | Name               | Position   | City           | Votes  | 
| ------------ |--------------------|------------|----------------|--------| 
| 240000609724 | COMANDANTE MOISÉS  | Governador | FLORIANÓPOLIS  | 236074 |
| 240000621321 | GELSON MERÍSIO     | Governador | FLORIANÓPOLIS  | 139731 |
| 240000609537 | MAURO MARIANI      | Governador | FLORIANÓPOLIS  |  43796 |
| 240000624336 | DÉCIO LIMA         | Governador | FLORIANÓPOLIS  |  39144 |
| 240000601841 | CAMASÃO            | Governador | FLORIANÓPOLIS  |  19362 |
| 240000616318 | PORTANOVA          | Governador | FLORIANÓPOLIS  |   4844 |
| 240000610038 | INGRID ASSIS       | Governador | FLORIANÓPOLIS  |   1644 |
| 240000614244 | JESSE PEREIRA      | Governador | FLORIANÓPOLIS  |   1281 |


### Authors

  * [Darlan Dal-Bianco](mailto:darlan@renovabr.org)
  * [Ederson Corbari](mailto:ederson@renovabr.org)
