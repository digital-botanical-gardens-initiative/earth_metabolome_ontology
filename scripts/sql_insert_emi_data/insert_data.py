from typing import Union
from mysql.connector import *
from mysql.connector.pooling import PooledMySQLConnection
from tqdm import tqdm
from matchms.importing import load_from_mgf
from matchms.filtering import add_precursor_mz, add_losses, normalize_intensities, reduce_to_number_of_peaks
from spec2vec import SpectrumDocument
import os
import networkx as nx


class SQLDataInsertion:

    @staticmethod
    def read_file(file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = file.read()
                file.close()
        else:
            data = False
        return data

    @staticmethod
    def sql_insert_emi_data(directory_path: str, table_name: str, name_suffix: str,
                            sql_db: Union[PooledMySQLConnection, MySQLConnection, CMySQLConnection, None],
                            name_prefix: str = None, ionization: str = "pos", terminated_by: str = '\t'):
        sample_folder_list = [folder for folder in os.listdir(directory_path)]
        db_cursor = sql_db.cursor()
        for sample_folder in tqdm(sample_folder_list):
            sample_dir = os.path.join(directory_path, sample_folder)
            if name_prefix is None:
                metadata_file_name = sample_folder + name_suffix
                absolut_file_path = os.path.join(sample_dir, metadata_file_name)
            else:
                relative_file_path = name_prefix + sample_folder + name_suffix
                absolut_file_path = os.path.join(sample_dir, relative_file_path)
            if os.path.isfile(absolut_file_path):
                if table_name == "molecular_network":
                    graph = nx.read_graphml(absolut_file_path)
                    sql_statement = "INSERT INTO " + table_name + "(source_id, target_id, weight," \
                                                                  " sample_id, ionization)  VALUES \n"
                    for attribute in graph.edges(data=True):
                        source_id = attribute[0]
                        target_id = attribute[1]
                        weight = attribute[2]['weight']
                        sql_statement += "('" + source_id + "','" + target_id + "','" + str(weight) + "','" \
                                         + sample_folder + "','" + ionization + "'),\n"
                    sql_statement = sql_statement[:-2] + ";"
                    db_cursor.execute(sql_statement)
                elif table_name == "spec2vec_doc":
                    spectra = Spectra(absolut_file_path)
                    for spectrum, document in spectra.spectrum_document_list:
                        feature_id = str(spectrum.metadata['feature_id'])
                        raw_spectrum = str(tuple(zip(spectrum.mz, spectrum.intensities)))
                        sql_statement = "INSERT INTO " + table_name + "(feature_id, raw_spectrum, word," \
                                                                      " sample_id, ionization)  VALUES \n"
                        for word in document:
                            sql_statement += "('" + feature_id + "','" + raw_spectrum + "','" + str(word) + "','" \
                                             + sample_folder + "','" + ionization + "'),\n"
                    sql_statement = sql_statement[:-2] + ";"
                    db_cursor.execute(sql_statement)
                else:
                    sql_statement = "LOAD DATA LOCAL INFILE '" + absolut_file_path + \
                                    "'  INTO TABLE " + table_name + " FIELDS terminated by '" + terminated_by \
                                    + "' optionally enclosed by '\"' IGNORE 1 LINES;\n"
                    db_cursor.execute(sql_statement)
                    if table_name == "sample_metadata":
                        method_file_name = sample_folder + '_lcms_method_params_' + ionization + '.txt'
                        params = SQLDataInsertion.read_file(os.path.join(sample_dir, ionization, method_file_name))
                        if params:
                            lcms_method_params = ", lcms_method_params = '" + params + "'"
                        else:
                            lcms_method_params = ''
                        sql_statement = "UPDATE " + table_name + " SET ionization = '" + ionization + \
                                        "' " + lcms_method_params + "where sample_id = '" \
                                        + sample_folder + "' AND ionization is NULL ;"
                        db_cursor.execute(sql_statement)
                    elif table_name != "taxon_metadata":
                        sql_statement = "UPDATE " + table_name + " SET sample_id = '" + sample_folder + "'," + \
                                        "ionization = '" + ionization + "' WHERE sample_id is NULL ;"
                        db_cursor.execute(sql_statement)
        db_cursor.close()


class Spectra:

    def __init__(self, mgf_file_path) -> None:
        super().__init__()
        self.spectra = self.load_and_filter_from_mgf(mgf_file_path)
        self.spectrum_document_list = list(self.get_spectrum_document_zip())

    @staticmethod
    def apply_filters(spectrum):
        spectrum = add_precursor_mz(spectrum)
        spectrum = normalize_intensities(spectrum)
        spectrum = reduce_to_number_of_peaks(spectrum, n_required=1, n_max=100)
        spectrum = add_precursor_mz(spectrum)
        spectrum = add_losses(spectrum, loss_mz_from=10, loss_mz_to=250)
        return spectrum

    def load_and_filter_from_mgf(self, path) -> list:
        """Load and filter spectra from mgf file
        Returns:
            spectrums (list of matchms.spectrum): a list of matchms.spectrum objects
        """
        spectra_list = [self.apply_filters(s) for s in load_from_mgf(path)]
        spectra_list = [s for s in spectra_list if s is not None]
        return spectra_list

    def get_spectrum_document_zip(self) -> zip:
        spectra_list = self.spectra
        reference_documents = [SpectrumDocument(s, n_decimals=2) for s in spectra_list]
        list_peaks_losses = list(doc.words for doc in reference_documents)
        return zip(spectra_list, list_peaks_losses)
