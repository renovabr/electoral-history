# Brazilian Electoral History

<p align="center"> 
<a href="https://www.renovabr.org">
<img border="0" alt="RenovaBR Foundation" src="https://raw.githubusercontent.com/renovabr/electoral-history/master/doc/img/renovabr.png">
</a>
</p>

Importation and standardization of the Electoral History of the Brazilian TSE

Available years are: *2010, 2012, 2014, 2016, 2018*

The script below downloads the TSE raw data. 

1. ./tse-data.sh 2010

for i in "2010" "2012" "2014" "2016" "2018"; do ./tse-data.sh ${i}; done

The data is downloaded in the project folder at: *data/tse/YEAR*

