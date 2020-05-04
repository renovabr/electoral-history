--
-- 01 - Table used by script (consulta_cand_xxxx)
--
DROP TABLE IF EXISTS raw_tse_consult_candidates;

CREATE TABLE raw_tse_consult_candidates (
    raw_tse_consult_candidates_id BIGINT NOT NULL AUTO_INCREMENT,
    dt_tse_generation DATE NOT NULL,
    hh_tse_generation TIME NOT NULL,
    election_year ENUM('2010', '2012', '2014', '2016', '2018') NOT NULL,
 	type_election TINYINT UNSIGNED NOT NULL,
    nm_type_election VARCHAR(50) NOT NULL,
	nr_shift TINYINT UNSIGNED NOT NULL,   
	cd_election SMALLINT UNSIGNED NOT NULL,
	ds_election VARCHAR(50) NOT NULL,
	dt_election DATE NOT NULL,
	tp_coverage VARCHAR(50) NOT NULL,
	sg_uf CHAR(2) NOT NULL,
	sg_ue VARCHAR(50) NOT NULL,
	nm_ue VARCHAR(50) NOT NULL,
	cd_position TINYINT UNSIGNED  NOT NULL,
	ds_position VARCHAR(100) NOT NULL,
	sq_candidate BIGINT NOT NULL,
	nr_candidate MEDIUMINT NOT NULL,
	nm_candidate VARCHAR(100) NOT NULL,
	nm_ballot_candidate VARCHAR(100) NOT NULL,
	nm_social_candidate VARCHAR(100) NOT NULL,
	nr_cpf_candidate CHAR(11) NOT NULL,
	nm_email VARCHAR(100) NOT NULL,
	cd_situ_cand TINYINT NOT NULL,
	ds_situ_cand VARCHAR(100) NOT NULL,
	cd_detail_situ_cand TINYINT NOT NULL,
	ds_detail_situ_cand VARCHAR(100) NOT NULL,
	tp_association VARCHAR(100) NOT NULL,
	nr_party TINYINT NOT NULL,
	sg_party VARCHAR(100) NOT NULL,
	nm_party VARCHAR(100) NOT NULL,
	sq_alliance BIGINT NOT NULL,
	nm_alliance VARCHAR(100) NOT NULL,
	ds_comp_alliance VARCHAR(500) NOT NULL,
	cd_nationality TINYINT NOT NULL,
	ds_nationality VARCHAR(100) NOT NULL,
	sg_uf_birth VARCHAR(100) NOT NULL,
	cd_city_birth TINYINT NOT NULL,
	nm_city_birth VARCHAR(100) NOT NULL,
	dt_birth VARCHAR(50) DEFAULT NULL,
	nr_age_date_inauguration VARCHAR(100) DEFAULT NULL,
	nr_doc_electoral_cand VARCHAR(100) NOT NULL,
	cd_genre TINYINT NOT NULL,
	ds_genre VARCHAR(100) NOT NULL,
	cd_degree_instruction TINYINT NOT NULL,
	ds_degree_instruction VARCHAR(100) NOT NULL,
	cd_marital_status TINYINT NOT NULL,
	ds_marital_status VARCHAR(100) NOT NULL,
	cd_race_color TINYINT NOT NULL,
	ds_race_color VARCHAR(100) NOT NULL,
	cd_occupation SMALLINT NOT NULL,
	ds_occupation VARCHAR(100) NOT NULL,
	nr_campaign_max_expenditure INT NOT NULL,
	cd_situ_tot_shift TINYINT NOT NULL,
	ds_situ_tot_shift VARCHAR(100) NOT NULL,
	st_reelection VARCHAR(100) NOT NULL,
	st_declare_goods VARCHAR(100) NOT NULL,
	nr_protocol_cand VARCHAR(100) NOT NULL,
	nr_process VARCHAR(100) NOT NULL,
	end_partition TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (raw_tse_consult_candidates_id, end_partition))
PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

ALTER TABLE raw_tse_consult_candidates PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),
    PARTITION p2020 VALUES LESS THAN (UNIX_TIMESTAMP('2020-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

SELECT COUNT(*) FROM raw_tse_consult_candidates PARTITION (p2010);
SELECT * FROM raw_tse_consult_candidates LIMIT 10;

--
-- 02 - Table used by script (votacao_candidato_munzona_xxxx)
--
DROP TABLE IF EXISTS raw_tse_voting_cand_city;

CREATE TABLE raw_tse_voting_cand_city (
    raw_tse_voting_cand_city_id BIGINT NOT NULL AUTO_INCREMENT,
	dt_tse_generation DATE NOT NULL,
	hh_tse_generation TIME NOT NULL,
	election_year ENUM('2010', '2012', '2014', '2016', '2018') NOT NULL,
	type_election TINYINT UNSIGNED NOT NULL,
	nm_type_election VARCHAR(50) NOT NULL,
	nr_shift TINYINT UNSIGNED NOT NULL,
	cd_election SMALLINT UNSIGNED NOT NULL,
	ds_election VARCHAR(50) NOT NULL,
	dt_election DATE NOT NULL,
	tp_coverage VARCHAR(50) NOT NULL,
	sg_uf CHAR(2) NOT NULL,
	sg_ue VARCHAR(50) NOT NULL,
	nm_ue VARCHAR(50) NOT NULL,
    cd_city MEDIUMINT NOT NULL,
	nm_city VARCHAR(100) NOT NULL,
	nr_zone MEDIUMINT NOT NULL,
	cd_position TINYINT UNSIGNED NOT NULL,
	ds_position VARCHAR(100) NOT NULL,
	sq_candidate BIGINT NOT NULL,
	nr_candidate MEDIUMINT NOT NULL,
	nm_candidate VARCHAR(100) NOT NULL,
	nm_ballot_candidate VARCHAR(100) NOT NULL,
	nm_social_candidate VARCHAR(100) NOT NULL,
	cd_situ_cand TINYINT NOT NULL,
	ds_situ_cand VARCHAR(100) NOT NULL,
	cd_detail_situ_cand	TINYINT NOT NULL,
	ds_detail_situ_cand	VARCHAR(100) NOT NULL,
	tp_association	VARCHAR(100) NOT NULL,
	nr_party TINYINT NOT NULL,
	sg_party VARCHAR(100) NOT NULL,
	nm_party VARCHAR(100) NOT NULL,
	sq_alliance BIGINT NOT NULL,
	nm_alliance VARCHAR(100) NOT NULL,
	ds_comp_alliance VARCHAR(500) NOT NULL,
	cd_situ_tot_shift TINYINT NOT NULL,
	ds_situ_tot_shift VARCHAR(100) NOT NULL,
	st_vote_in_transit VARCHAR(100) NOT NULL,
	qt_votes_nominal INT NOT NULL,
	end_partition TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (raw_tse_voting_cand_city_id, end_partition))
PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

ALTER TABLE raw_tse_voting_cand_city PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),
    PARTITION p2020 VALUES LESS THAN (UNIX_TIMESTAMP('2020-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

SELECT COUNT(*) FROM raw_tse_voting_cand_city PARTITION (p2014);
SELECT * FROM raw_tse_voting_cand_city LIMIT 10;

--
-- 03 - Table used by script (votacao_partido_munzona_xxxx)
--
DROP TABLE IF EXISTS raw_tse_voting_party_city;

CREATE TABLE raw_tse_voting_party_city (
	raw_tse_voting_party_city_id BIGINT NOT NULL AUTO_INCREMENT,
	dt_tse_generation DATE NOT NULL,
    hh_tse_generation TIME NOT NULL,
    election_year ENUM('2010', '2012', '2014', '2016', '2018') NOT NULL,
 	type_election TINYINT UNSIGNED NOT NULL,
    nm_type_election VARCHAR(50) NOT NULL,
	nr_shift TINYINT UNSIGNED NOT NULL,   
	cd_election SMALLINT UNSIGNED NOT NULL,
	ds_election VARCHAR(50) NOT NULL,
	dt_election DATE NOT NULL,
	tp_coverage VARCHAR(50) NOT NULL,
	sg_uf CHAR(2) NOT NULL,
	sg_ue VARCHAR(50) NOT NULL,
	nm_ue VARCHAR(50) NOT NULL,
    cd_city MEDIUMINT NOT NULL,
	nm_city VARCHAR(100) NOT NULL,
	nr_zone MEDIUMINT NOT NULL,
	cd_position TINYINT UNSIGNED  NOT NULL,
	ds_position VARCHAR(100) NOT NULL,
	tp_association VARCHAR(100) NOT NULL,
	nr_party TINYINT NOT NULL,
	sg_party VARCHAR(100) NOT NULL,
	nm_party VARCHAR(100) NOT NULL,
	sq_alliance BIGINT NOT NULL,
	nm_alliance VARCHAR(100) NOT NULL,
	ds_comp_alliance VARCHAR(500) NOT NULL,
	st_vote_in_transit VARCHAR(100) NOT NULL,
	qt_votes_nominal INT NOT NULL,
	qt_votes_legend INT NOT NULL,
	end_partition TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (raw_tse_voting_party_city_id, end_partition))
PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

ALTER TABLE raw_tse_voting_party_city PARTITION BY RANGE (UNIX_TIMESTAMP(end_partition)) (
    PARTITION p2010 VALUES LESS THAN (UNIX_TIMESTAMP('2010-12-31 23:59:59')),
    PARTITION p2012 VALUES LESS THAN (UNIX_TIMESTAMP('2012-12-31 23:59:59')),
    PARTITION p2014 VALUES LESS THAN (UNIX_TIMESTAMP('2014-12-31 23:59:59')),
    PARTITION p2016 VALUES LESS THAN (UNIX_TIMESTAMP('2016-12-31 23:59:59')),
    PARTITION p2018 VALUES LESS THAN (UNIX_TIMESTAMP('2018-12-31 23:59:59')),
    PARTITION p2020 VALUES LESS THAN (UNIX_TIMESTAMP('2020-12-31 23:59:59')),    
    PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

SELECT COUNT(*) FROM raw_tse_voting_party_city PARTITION (p2014);
SELECT * FROM raw_tse_voting_party_city LIMIT 10;
