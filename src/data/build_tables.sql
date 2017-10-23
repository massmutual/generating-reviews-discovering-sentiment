DROP TABLE IF EXISTS voc.all;
CREATE TABLE voc.all (
	source VARCHAR(64),
	type VARCHAR(64),
	datetime TIMESTAMP,
	source_id VARCHAR(128),
	source_id_column VARCHAR(64),
	raw_text VARCHAR(300),
	clean_text VARCHAR(300)
);



INSERT INTO voc.all (
	source, 
	type, 
	datetime,
	source_id, 
	source_id_column, 
	raw_text)
(SELECT distinct 'voc.confirmit_Newcustomer',
	'survey',
	ResponseDate::TIMESTAMP,
	ResponseID,
	'ResponseID',
	additionalComments
	from voc.confirmit_Newcustomer
	where trim(additionalComments) is not null);


INSERT INTO voc.all (
	source, 
	type, 
	datetime,
	source_id, 
	source_id_column, 
	raw_text)
(SELECT distinct 'voc.confirmit_RSWorksite',
	'survey',
	ResponseDate::TIMESTAMP,
	ResponseID,
	'ResponseID',
	ReasonOther2
	from voc.confirmit_RSWorksite
	where trim(ReasonOther2) is not null);



INSERT INTO voc.all (
	source, 
	type, 
	source_id, 
	source_id_column, 
	raw_text)
(SELECT distinct 'voc.confirmit_UATClaims',
	'survey',
	ResponseID,
	'ResponseID',
	Verbatim
	from voc.confirmit_UATClaims
	where trim(Verbatim) is not null);


INSERT INTO voc.all (
	source, 
	type, 
	datetime,
	source_id, 
	source_id_column, 
	raw_text)
(SELECT distinct 'voc.confirmit_annuity',
	'survey',
	ResponseDate,
	ResponseID,
	'ResponseID',
	Experience_comment
	from voc.confirmit_annuity
	where trim(Experience_comment) is not null);

INSERT INTO voc.all (
	source, 
	type, 
	datetime,
	source_id, 
	source_id_column, 
	raw_text)
(SELECT distinct 'voc.confirmit_ebppppe',
	'survey',
	ResponseDate,
	ResponseID,
	'ResponseID',
	Q7
	from voc.confirmit_ebppppe
	where trim(Q7) is not null);
