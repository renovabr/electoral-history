<img src="doc/img/brazil-vector.png" align="right" width="180" height="180"/>

# Brazilian Electoral History

<p align="center"> 
<a href="https://www.renovabr.org">
<img border="0" alt="RenovaBR Foundation" src="https://raw.githubusercontent.com/renovabr/electoral-history/master/doc/img/renovabr.png">
</a>
</p>

[ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) project that collects data from the **Brazilian Electoral Data Repository** and imports it into a **MySQL** database, and then the data is placed in **Elasticsearch** using the ELK stack. Electoral years available: *2010, 2012, 2014, 2016, 2018*. The full import of every year totals **24.340.098** million lines in the database.

## Synopsis

This is a raw data processing ([ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load)) project for standardizing information for a **MySQL** Database. The Brazilian Electoral History data is made available by **TSE** on the website [TSE Electoral Data Repository](http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais).

The process of importing the data into an SQL database aims to facilitate the development of other systems as well as for statistical analysis.

### Architecture

This project uses the following technologies:

  * [MySQL](https://www.mysql.com/)
  * [Python](https://www.python.org/)
  * [ELK](https://www.elastic.co/)

<p align="center"> 
<img src="https://raw.githubusercontent.com/renovabr/electoral-history/master/doc/img/electoral-history.png">
</p>

Three tables are created in the database called (*electoral_history*) to store the data. Are they:

| Table                       | Lines      | Description
| --------------------------- | ---------- |---------------------------------------- | 
| raw_tse_consult_candidates  | 10.600.43  | Contains all candidates.                |
| raw_tse_voting_cand_city    | 20.7102.63 | Contains candidate votes by city.       |
| raw_tse_voting_party_city   | 16.044.42  | Contains party votes by city.           |
| raw_tse_cand_goods_declared | 21.302.42  | Contains the goods declared candidates. |
| cand_info                   | 6.460.79   | Merge with candidate information.       |

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

The **tse-data** script downloads the raw data using the year as a parameter. Example to download the year 2010:

```shell
$ ./tse-data 2010
```

You can also download them all using the command:

```shell
$ for i in "2010" "2012" "2014" "2016" "2018"; do ./tse-data ${i}; done
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

>Note: A database will be created called: *electoral_historal* with three tables and a user with access to a database called *winston*. The database connection settings can be changed in the *config.ini* file.

#### 3. Import all data to MySQL 

To import the **candidates data** for all years, use the script: **run-import-all**.

```shell
$ ./01-run-import-all 'consulta-cand'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./01-consulta-cand.py -y 2010 -s 'SP' \
  -p ../data/tse/2010/consulta_cand_2010/ -e txt
```

The same procedure applies to the other tables. To import all **candidates voting** data, use the command:

```shell
$ ./01-run-import-all 'votacao-candidato'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./02-votacao-candidato-munzona.py -y 2010 -s 'SP' -p \
  ../data/tse/2010/votacao_candidato_munzona_2010/ -e txt
```

For the import of **votes by party**:

```shell
$ ./01-run-import-all 'votacao-partido'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./03-votacao-partido-munzona.py -y 2010 -s 'SC' \
  -p ../data/tse/2010/votacao_partido_munzona_2010/ -e txt
```

To import candidates' **declared goods**:

```shell
$ ./01-run-import-all 'bem-candidato'
```

If you want to import a specific year and state you can use the command:

```shell
$ cd src
$ ./04-bens-candidato.py -y 2010 -s 'SC' \
  -p ../data/tse/2010/bem_candidato_2010/ -e txt
```

#### 4. Computing candidate votes and information 

This table is a merge with the candidate base and the voting base by zone.

```shell
$ cd src
$ ./04-cand-info.py -y 2010 
```

If you want to listen to only one state and save it in a CSV file, use the command:

```shell
$ cd src
$ ./04-cand-info.py -y 2018 -s SC -e data.csv
```

To process every year use the command:

```shell
$ cd src
$ for i in "2010" "2012" "2014" "2016" "2018"; do ./04-cand-info.py -y ${i}; done
```

The script must be executed per year and the results are saved in table *cand_info*

#### 5. Checking and analyzing data 

There is a data dictionary that can be downloaded here: [Dictionary](doc/dictionary-data.xlsx). 

All tables are partitioned by the year of election.

```sql
SELECT COUNT(1) FROM raw_tse_consult_candidates PARTITION (p2010);
```

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

| 2016     |
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

| 2018     |
| -------- | 
| Deputado Distrital |
| Deputado Estadual  |
| Deputado Federal   |
| Governador         |
| Senador            |

Checking the total number of votes of the Governors of the state of Santa Catarina in the city of *Florianópolis* in the first shift of the 2018 elections.

```sql
SELECT
  sq_candidate AS SQ,
  nm_ballot_candidate AS Name,
  ds_position AS Position,
  nm_city AS City,
  format(sum(qt_votes_nominal), 0, 'de_DE') AS Votes 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
  AND sg_uf = 'SC' 
  AND cd_city = 81051 
  AND nr_shift = 1 
  AND cd_position = 3 
GROUP BY
  1,
  2,
  3,
  4 
ORDER BY
  sum(qt_votes_nominal) DESC;
```

| SQ           | Name               | Position   | City           | Votes  | 
| ------------ |--------------------|------------|----------------|--------| 
| 240000609724 | COMANDANTE MOISÉS  | Governador | FLORIANÓPOLIS  | 73.947 |
| 240000621321 | GELSON MERÍSIO     | Governador | FLORIANÓPOLIS  | 59.524 |
| 240000609537 | MAURO MARIANI      | Governador | FLORIANÓPOLIS  | 43.796 |
| 240000624336 | DÉCIO LIMA         | Governador | FLORIANÓPOLIS  | 39.144 |
| 240000601841 | CAMASÃO            | Governador | FLORIANÓPOLIS  | 19.362 |
| 240000616318 | PORTANOVA          | Governador | FLORIANÓPOLIS  | 4.844  |
| 240000610038 | INGRID ASSIS       | Governador | FLORIANÓPOLIS  | 1.644  |
| 240000614244 | JESSE PEREIRA      | Governador | FLORIANÓPOLIS  | 1.281  |


Checking the total number of votes of the Governors of the State of *Santa Catarina* in the second shit of the 2018 elections.

```sql
SELECT
  sq_candidate AS SQ,
  nm_ballot_candidate AS Name,
  ds_position AS Position,
  format(sum(qt_votes_nominal), 0, 'de_DE') AS Votes 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
  AND sg_uf = 'SC' 
  AND nr_shift = 2 
  AND cd_position = 3 
GROUP BY
  1,
  2,
  3 
ORDER BY
  sum(qt_votes_nominal) DESC;
```  

| SQ           | Name               | Position   | Votes     | 
| ------------ |--------------------|------------|-----------| 
| 240000609724 | COMANDANTE MOISÉS  | Governador | 2.644.179 |
| 240000621321 | GELSON MERÍSIO     | Governador | 1.075.242 |


Checking the total number of votes of the Governors of the State of *São Paulo* in the first shift of the 
2018 elections.

```sql
SELECT
  sq_candidate AS SQ,
  nm_ballot_candidate AS Name,
  ds_position AS Position,
  format(sum(qt_votes_nominal), 0, 'de_DE') AS Votes 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
  AND sg_uf = 'SP' 
  AND nr_shift = 1 
  AND cd_position = 3 
GROUP BY
  1,
  2,
  3 
ORDER BY
  sum(qt_votes_nominal) DESC;
```

| SQ           | Name                   | Position   | Votes     | 
| ------------ |------------------------|------------|-----------| 
| 250000612596 | JOÃO DORIA             | Governador | 6.431.555 |
| 250000615141 | MARCIO FRANÇA          | Governador | 4.358.998 |
| 250000604077 | PAULO SKAF             | Governador | 4.269.865 |
| 250000623884 | LUIZ MARINHO           | Governador | 2.563.922 |
| 250000612133 | MAJOR COSTA E SILVA    | Governador | 747.462   |
| 250000601939 | ROGERIO CHEQUER        | Governador | 673.102   |
| 250000615464 | RODRIGO TAVARES        | Governador | 649.729   |
| 250000601522 | PROFESSORA LISETE      | Governador | 507.236   |
| 250000617766 | PROF. CLAUDIO FERNANDO | Governador | 28.666    |
| 250000609174 | TONINHO FERREIRA       | Governador | 16.202    |

Which top 10 city has the most votes for a distinguished candidate example the candidate (*250000612596*) to governor of the state of São Paulo, for the second shift.

```sql
SELECT
  nm_city AS City,
  sum(qt_votes_nominal) AS Votes 
FROM
  raw_tse_voting_cand_city 
WHERE
  election_year = '2018' 
  AND sg_uf = 'SP' 
  AND nr_shift = 2 
  AND cd_position = 3 
  AND sq_candidate = 250000612596 
GROUP BY
  1 
ORDER BY
  2 DESC LIMIT 10;
```

| City                   | Votes   | 
| ---------------------- |---------|
| SÃO PAULO              | 2447309 |
| CAMPINAS               |  315524 |
| GUARULHOS              |  240825 |
| SÃO JOSÉ DOS CAMPOS    |  232775 |
| SOROCABA               |  207470 |
| SANTO ANDRÉ            |  202125 |
| SÃO BERNARDO DO CAMPO  |  196202 |
| OSASCO                 |  176109 |
| RIBEIRÃO PRETO         |  166728 |
| JUNDIAÍ                |  143028 |

### Authors

  * [Darlan Dal-Bianco](mailto:darlan@renovabr.org)
  * [Ederson Corbari](mailto:ederson@renovabr.org)
  
