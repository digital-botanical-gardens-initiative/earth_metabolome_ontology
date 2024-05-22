# Raw data input file path
raw_data_root_folder = "data/output/individual_analysis"
ionization_mode = 'pos'
structure_metadata_sqlite_file = "data/structures_metadata.db"
# MySQL table mapping where values are mysql table names corresponding to the dictionary keys
table_canonical_names = {'compound_summary': 'canopus_compound_summary',
                         'sample_metadata': 'sample_metadata',
                         'taxon_metadata': 'taxon_metadata',
                         'features_quant': 'features_quant',
                         'compound_identifications': 'compound_identifications',
                         'isdb_reweighted_flat': 'isdb_reweighted_flat',
                         'molecular_network': 'molecular_network',
                         'molecular_network_metadata': 'molecular_network_metadata',
                         'spec2vec_doc': 'spec2vec_doc',
                         'structures_metadata': 'structures_metadata'
                         }

# MySQL db credentials
host = "localhost"
user = "root"
password = "root_mysql"
database = "emi_db"
port = "3306"
