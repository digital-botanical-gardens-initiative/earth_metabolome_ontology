CREATE DATABASE IF NOT EXISTS `emi_db`;
USE `emi_db`;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `canopus_compound_summary`;
CREATE TABLE canopus_compound_summary (
	id VARCHAR(255)  , 
	`molecularFormula` VARCHAR(255) , 
	adduct VARCHAR(255) , 
	#`precursorFormula` VARCHAR(255) , #removed
	`NPC_pathway` VARCHAR(255) , 
	`NPC_pathway_Probability` DOUBLE , 
	`NPC_superclass` VARCHAR(255) , 
	`NPC_superclass_Probability` DOUBLE , 
	`NPC_class` VARCHAR(255) , 
	`NPC_class_Probability` DOUBLE , 
	`ClassyFire_most_specific_class` VARCHAR(255) , 
	`ClassyFire_most_specific_class_Probability` DOUBLE , 
	`ClassyFire_level_5` VARCHAR(255), 
	`ClassyFire_level_5_Probability` DOUBLE, 
	`ClassyFire_subclass` VARCHAR(255), 
	`ClassyFire_subclass_Probability` DOUBLE, 
	`ClassyFire_class` VARCHAR(255), 
	`ClassyFire_class_Probability` DOUBLE, 
	`ClassyFire_superclass` VARCHAR(255) , 
	`ClassyFire_superclass_probability` DOUBLE , 
	`ClassyFire_all_classifications` VARCHAR(2550) , 
	#`featureId` INT, #removed
    sample_id VARCHAR(255),
	ionization VARCHAR(255),
    PRIMARY KEY (id) #,
   #FOREIGN KEY (sample_id) REFERENCES sample_metadata(sample_id) 
) #ENGINE = MEMORY
;

DROP TABLE IF EXISTS `sample_metadata`;
CREATE TABLE `sample_metadata` (
	sample_id VARCHAR(255), 
	sample_type VARCHAR(255) , 
	source_id VARCHAR(255) COMMENT 'renamed: sample_substance_name',
	organism_kingdom VARCHAR(255) , 
	organism_phylum VARCHAR(255) , 
	organism_class VARCHAR(255) , 
	organism_order VARCHAR(255) , 
	organism_family VARCHAR(255) , 
	organism_genus VARCHAR(255) , 
	source_taxon VARCHAR(255) COMMENT 'renamed: organism_species',   
	organism_organe VARCHAR(255) , 
	organism_broad_organe VARCHAR(255) , 
	organism_tissue VARCHAR(255) , 
	organism_subsystem VARCHAR(255) , 
	sample_plate_id VARCHAR(255) , 
	sample_filename_pos VARCHAR(255) , 
	pos_injection_date DATE , 
	bio_leish_donovani_10ugml_inhibition DOUBLE , 
	bio_leish_donovani_2ugml_inhibition DOUBLE , 
	bio_tryp_brucei_rhodesiense_10ugml_inhibition DOUBLE , 
	bio_tryp_brucei_rhodesiense_2ugml_inhibition DOUBLE , 
	bio_tryp_cruzi_10ugml_inhibition DOUBLE , 
	bio_l6_cytotoxicity_10ugml_inhibition DOUBLE , 
	sample_filename_neg VARCHAR(255) , 
	neg_injection_date DATE , 
	massive_id VARCHAR(255) ,
    ionization VARCHAR(255),
    lcms_method_params TEXT,
	PRIMARY KEY (sample_id));
    
DROP TABLE IF EXISTS `taxon_metadata`;
CREATE TABLE taxon_metadata (
	a BOOL, 
	sample_id VARCHAR(255), 
	sample_type TEXT, 
	source_id TEXT COMMENT 'renamed: sample_substance_name', 
	organism_kingdom TEXT, 
	organism_phylum TEXT, 
	organism_class TEXT, 
	organism_order TEXT, 
	organism_family TEXT, 
	organism_genus TEXT, 
	source_taxon TEXT COMMENT 'renamed: organism_species',  
	organism_organe TEXT, 
	organism_broad_organe TEXT, 
	organism_tissue TEXT, 
	organism_subsystem TEXT, 
	sample_plate_id TEXT, 
	sample_filename_pos TEXT, 
	pos_injection_date DATE, 
	bio_leish_donovani_10ugml_inhibition DOUBLE, 
	bio_leish_donovani_2ugml_inhibition DOUBLE, 
	bio_tryp_brucei_rhodesiense_10ugml_inhibition DOUBLE, 
	bio_tryp_brucei_rhodesiense_2ugml_inhibition DOUBLE, 
	bio_tryp_cruzi_10ugml_inhibition DOUBLE, 
	bio_l6_cytotoxicity_10ugml_inhibition DOUBLE, 
	sample_filename_neg TEXT, 
	neg_injection_date DATE, 
	massive_id TEXT, 
	is_approximate_match BOOL, 
	is_synonym BOOL , 
	matched_name TEXT, 
	nomenclature_code VARCHAR(255), 
	score DOUBLE, 
	search_string TEXT, 
	taxon_flags TEXT, 
	taxon_is_suppressed BOOL , 
	taxon_is_suppressed_from_synth BOOL , 
	taxon_name TEXT, 
	taxon_ott_id DOUBLE , 
	taxon_rank TEXT, 
	taxon_source TEXT, 
	taxon_synonyms TEXT, 
	taxon_tax_sources TEXT, 
	taxon_unique_name TEXT, 
	_merge TEXT, 
	ott_id DOUBLE , 
	query_otol_domain TEXT, 
	query_otol_kingdom TEXT, 
	query_otol_phylum TEXT, 
	query_otol_class TEXT, 
	query_otol_order TEXT, 
	query_otol_family TEXT, 
	query_otol_tribe TEXT, 
	query_otol_genus TEXT, 
	query_otol_species TEXT, 
	ott_type TEXT, 
	ott_value DOUBLE , 
	wd_type TEXT, 
	wd_value TEXT, 
	img_type TEXT, 
	img_value TEXT,
    PRIMARY KEY (sample_id)
);

DROP TABLE IF EXISTS `features_quant`;
CREATE TABLE features_quant (
	row_ID int,
    row_mz double,
    row_retention_time double,
    peak_area double,
    ionization VARCHAR(255),
    sample_id VARCHAR(255)

);

DROP TABLE IF EXISTS `compound_identifications`;
CREATE TABLE compound_identifications (
	`rank` INT COMMENT 'previous name: confidenceRank', 
#	`structurePerIdRank` INT , #removed
	`formulaRank` INT ,  
	`#adducts` INT ,  
	`#predictedFPs` DOUBLE ,  
	`ConfidenceScore` DOUBLE, 
	`CSI:FingerIDScore` DOUBLE ,  
	`ZodiacScore` DOUBLE ,  
	`SiriusScore` DOUBLE ,  
	`molecularFormula` TEXT ,  
	adduct VARCHAR(255) ,  
	`InChIkey2D` VARCHAR(14) ,  
	`InChI` TEXT ,  
	name TEXT, 
	smiles TEXT ,  
	xlogp DOUBLE ,  
	pubchemids TEXT, 
	links TEXT ,  
	dbflags DOUBLE ,  
	`ionMass` DOUBLE ,  
	`retentionTimeInSeconds` DOUBLE ,  
	id VARCHAR(1000) NOT NULL,  
	#`featureId` INT NOT NULL, #removed
	sample_id VARCHAR(1000),
	ionization VARCHAR(255)
);

DROP TABLE IF EXISTS isdb_reweighted_flat ;
CREATE TABLE `isdb_reweighted_flat` (
	a INT , 
	featureId INT , 
	component_id INT , 
	structure_taxonomy_npclassifier_01pathway_consensus TEXT, 
	freq_structure_taxonomy_npclassifier_01pathway DOUBLE, 
	structure_taxonomy_npclassifier_02superclass_consensus TEXT, 
	freq_structure_taxonomy_npclassifier_02superclass DOUBLE, 
	structure_taxonomy_npclassifier_03class_consensus TEXT, 
	freq_structure_taxonomy_npclassifier_03class DOUBLE, 
	rank_spec INT , 
	score_input DOUBLE , 
	libname TEXT , 
	short_inchikey TEXT , 
	`structure_smiles_2D` TEXT, 
	structure_molecular_formula TEXT, 
	adduct TEXT, 
	structure_exact_mass DOUBLE, 
	structure_taxonomy_npclassifier_01pathway TEXT, 
	structure_taxonomy_npclassifier_02superclass TEXT, 
	structure_taxonomy_npclassifier_03class TEXT, 
	query_otol_species TEXT , 
	lowest_matched_taxon TEXT, 
	score_taxo INT , 
	score_max_consistency INT , 
	final_score DOUBLE , 
	rank_final INT ,
	sample_id VARCHAR(1000),
	ionization VARCHAR(255)
);

DROP TABLE IF EXISTS molecular_network ;
CREATE TABLE `molecular_network` (
	source_id INT NOT NULL, 
	target_id INT NOT NULL, 
	weight DOUBLE ,
    sample_id VARCHAR(1000),
	ionization VARCHAR(255)
    );

DROP TABLE IF EXISTS molecular_network_metadata ;
CREATE TABLE `molecular_network_metadata` (
	feature_id INT,
	component_id INT,
	precursor_mz DOUBLE,
    sample_id VARCHAR(1000),
	ionization VARCHAR(255)
    );
    
DROP TABLE IF EXISTS spec2vec_doc ;
CREATE TABLE `spec2vec_doc` (
	feature_id INT,
    raw_spectrum TEXT,
    word TEXT,
    sample_id VARCHAR(1000),
	ionization VARCHAR(255)
    );
    
DROP TABLE IF EXISTS structures_metadata ;

SET FOREIGN_KEY_CHECKS = 1;