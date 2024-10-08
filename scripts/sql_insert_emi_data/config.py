# Raw data input file path
raw_data_root_folder = "data/output/individual_analysis"
#if an empty string or None does not consider it 
open_tree_of_life_dir = None
#if an empty string or None does not consider it
trait_dir = None
ionization_mode = 'pos'
structure_metadata_sqlite_file = "data/structures_metadata.db"
# MySQL table mapping where values are mysql table names corresponding to the dictionary keys
#For trait_data: tables names should be exactly the same as the file names without file extension
table_canonical_names = {'compound_summary': 'canopus_compound_summary',
                         'sample_metadata': 'sample_metadata',
                         'taxon_metadata': 'taxon_metadata',
                         'features_quant': 'features_quant',
                         'compound_identifications': 'compound_identifications',
                         'isdb_reweighted_flat': 'isdb_reweighted_flat',
                         'molecular_network': 'molecular_network',
                         'molecular_network_metadata': 'molecular_network_metadata',
                         'spec2vec_doc': 'spec2vec_doc',
                         'structures_metadata': 'structures_metadata',
                         'opentreeoflife': 'open_tree_life',
                         'opentreeoflife_synonym': 'open_tree_life_synonym',
                         'trait_data': { 'traits': 'traits',
                                    'trydbAll': 'trydbAll',
                                    'taxonomy': 'taxonomy',
                                    'enpkg': 'enpkg',
                                    'lotus': 'lotus',
                                    'interactions': 'interactions'}
                         }

# MySQL db credentials
host = "localhost"
user = "root"
password = "root"
database = "emi_db"
port = "3306"
