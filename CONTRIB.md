1. Download the toy dataset see ENPKG full (https://github.com/enpkg/enpkg_full)


Requirements 

MySQL https://dev.mysql.com/downloads/mysql/8.0.html

To check if correctly installed 



```bash
mysql --version
```
We install the Pipfile

```bash
cd scripts/sql_insert_emi_data
pipenv install
```



In case you have issue connecting check https://gist.github.com/zubaer-ahammed/c81c9a0e37adc1cb9a6cdc61c4190f52?permalink_comment_id=4473133

From the root of this directory
Create the Schema in the DB


```bash
mysql -u root -p < scripts/sql_insert_emi_data/raw_mysql_schema.sql
````


You can the connect 
    
```bash
mysql -u root -p
```

And then check if the schema was created

```sql
show databases;
use emi_db;
show tables;
```

Alternatively you can use the MYSQL Workbench to check the schema

```bash
mysql-workbench
```

We observe that the structure_metadata (sqlite) is missing for now.

We edit the scripts/sql_insert_emi_data/config.py file and make sure that the path are pointing to the correct files.




## Allow for insertion in mysql

Traceback (most recent call last):
  File "/Users/pma/.pyenv/versions/3.10.14/lib/python3.10/site-packages/mysql/connector/connection_cext.py", line 697, in cmd_query
    self._cmysql.query(
_mysql_connector.MySQLInterfaceError: Loading local data is disabled; this must be enabled on both the client and server sides

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/pma/Dropbox/git_repos/COMMONS_Lab/DBGI/earth_metabolome_ontology/scripts/sql_insert_emi_data/main.py", line 14, in <module>
    SQLDataInsertion.sql_insert_emi_data(
  File "/Users/pma/Dropbox/git_repos/COMMONS_Lab/DBGI/earth_metabolome_ontology/scripts/sql_insert_emi_data/insert_data.py", line 69, in sql_insert_emi_data
    db_cursor.execute(sql_statement)
  File "/Users/pma/.pyenv/versions/3.10.14/lib/python3.10/site-packages/mysql/connector/cursor_cext.py", line 372, in execute
    result = self._cnx.cmd_query(
  File "/Users/pma/.pyenv/versions/3.10.14/lib/python3.10/site-packages/mysql/connector/opentelemetry/context_propagation.py", line 102, in wrapper
    return method(cnx, *args, **kwargs)
  File "/Users/pma/.pyenv/versions/3.10.14/lib/python3.10/site-packages/mysql/connector/connection_cext.py", line 705, in cmd_query
    raise get_mysql_exception(
mysql.connector.errors.ProgrammingError: 3948 (42000): Loading local data is disabled; this must be enabled on both the client and server sides


```bash
mysql -u root -p
```

```sql
SHOW VARIABLES LIKE "local_infile";
SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE "local_infile";
```


Should return a 

mysql> SHOW VARIABLES LIKE "local_infile";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| local_infile  | ON    |
+---------------+-------+
1 row in set (0,01 sec)


Get Ontop

https://sourceforge.net/projects/ontop4obda/files/ontop-5.1.1/ontop-cli-5.1.1.zip/download

Get drivers for MySQL and SQLite

https://dev.mysql.com/downloads/connector/j/

Download the connectors for Ontop
https://downloads.mysql.com/archives/c-j/

move the archive mysql-connector-j-8.2.0.jar to the ontop-cli-5.1.1/lib folder

```bash
/Applications/ontop-cli-5.1.1/ontop materialize -m ./ontop_config/emi-v0_1.obda -t ./ontop_config/emi-v0_1.ttl -p ./ontop_config/emi-v0_1.properties -f turtle --enable-annotations  --separate-files -o ./data/ontop
````




