from typing import Union
from mysql.connector import *
from mysql.connector.pooling import PooledMySQLConnection
from tqdm import tqdm
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
