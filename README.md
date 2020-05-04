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

#### 1. Get the code

Now run the commands below to compile the project:

```shell
$ git clone https://github.com/renovabr/electoral-history.git
$ cd electoral-history
```

Enter pipenv at the root of the *electoral-history* folder for the tests:

```shell
$ pipenv shell
$ pipenv install
```


-----------------------------------------------------------
Importation and standardization of the Electoral History of the Brazilian TSE

Available years are: *2010, 2012, 2014, 2016, 2018*

The script below downloads the TSE raw data. 

1. ./tse-data.sh 2010

for i in "2010" "2012" "2014" "2016" "2018"; do ./tse-data.sh ${i}; done

The data is downloaded in the project folder at: *data/tse/YEAR*

### Authors

  * [Darlan Dal-Bianco <darlan at renovabr.org>](mailto:darlan@renovabr.org)
  * [Ederson Corbari <ederson at renovabr.org>](mailto:ederson@renovabr.org)
