# Raw data input file path
raw_data_root_folder = "/Documents/git_repositories/enpkg_full/tests/data/output"
ionization_mode = 'pos'
structure_metadata_sqlite_file = "/Documents/git_repositories/enpkg_full/05_enpkg_meta_analysis/structures_metadata.db"
# MySQL table mapping
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
password = ""
database = "emi_db"
port = "3306"
