from pandas import DataFrame, concat
from typing import List
from tqdm import tqdm
from pyspark.sql.session import SparkSession as spark
import pyspark.sql as sql

try:
    # up to DBR 8.2
    from dbutils import DBUtils  # pylint: disable=import-error,wrong-import-position
    NEW_DBUTILS = False
except:
    # above DBR 8.3
    from dbruntime.dbutils import DBUtils  # pylint: disable=import-error,wrong-import-position
    NEW_DBUTILS = True

from .exceptions import EmptyDataFrameException
from .decoradores import Singleton

@Singleton
class DeltaManager:
    def __init__(self, mounts = ["raw", "silver", "gold"]):
        # Inicializamos el dataframe de registro
        self.tables = None
        self.update()
        
    def mount(self, 
              storage:     str,
              key:         str,
              mount_point: str       = '/mnt/',
              mounts:      List[str] = ["raw", "silver", "gold"], 
              postfix:     str       = '-zone',
              include_tqdm:        bool      = False
              ):
        """
            This method let's you mount a set of different mounts at once. By default, 
            those values come as 'raw', 'silver' and 'gold'.
        """
        def __mount(mount_name: str):
            """
                This function let's you mount a single one. It works with the help of a 
                lambda function in order to run all mounts.
            """
            if not f"{mount_point}{mount_name}{postfix}" in list(map(lambda mount: mount.mountPoint, dbutils.fs.mounts())):
                dbutils.fs.mount(
                    source = f"wasbs://{mount_name}{postfix}@{storage}.blob.core.windows.net/",
                    mount_point = f"{mount_point}{mount_name}{postfix}",
                    extra_configs = { 
                        f"fs.azure.account.key.{storage}.blob.core.windows.net": key
                    }
                )

        if include_tqdm:
            list(map(lambda mount_name: __mount(mount_name), tqdm(mounts, desc="Mounts", position=0, leave=True)))
        else:
            list(map(lambda mount_name: __mount(mount_name), mounts))
            
    def update(self):
        """
            The update method reads what is currently up in the system.
        """
        nombre_tablas = list(map(lambda table: (table.name, table.database, table.description, table.tableType, table.isTemporary), sql.catalog.listTables()))
        
        self.tables = DataFrame(columns = ['name', 'database', 'path', 'type', 'is_temporary', 'description'])
        
        # Add new ones
        for nombre_tabla in nombre_tablas:
            if not nombre_tabla[0] in self.tables.name.to_list():
                self.tables = concat([self.tables, DataFrame([[nombre_tabla[0], nombre_tabla[1], sql(f"desc formatted {nombre_tabla[0]}").toPandas().set_index("col_name").drop("comment", axis = 1)["data_type"]["Location"], nombre_tabla[3], nombre_tabla[4], nombre_tabla[2]]], columns = ['name', 'database', 'path', 'type', 'is_temporary', 'description'])])
                
    def add(self, 
            table_name:   str,
            raw_path:     str,
            destionation_path: str,
            write_mode:   str  = 'overwrite',
            file_name:    str  = None,
            nested:       bool = False
            ):
        """
            This method adds a new table to the system.
        """
        # We read the data from the parquet into a dataframe. 
        if nested:
            df = spark.read.parquet(f"dbfs:{raw_path}{file_name}/{file_name}.parquet")
        else:
            df = spark.read.parquet(f"dbfs:{raw_path}{file_name}.parquet")
        
        # We check if there is data in the dataframe.
        if df.count() > 0:
            # Check if the table already exist, then we overwrite it.
            if table_name in [table.name for table in spark.catalog.listTables()]:
                df.write.mode(write_mode).format("delta").option("mergeSchema", "true").saveAsTable(table_name)
            else:
                # In case the table doesn't exist, we create it.
                try:
                    # We write the df in the destionation_path
                    df.write.format('delta').save(destionation_path)
                except Exception as error:
                    EOL = '\n'
                    raise Exception(f'Tried to {write_mode} the table and failed with the following message:{EOL}{error}')
                # Create the table.
                sql("CREATE TABLE " + table_name + " USING DELTA LOCATION " + f"'{destionation_path}{table_name}'" )
        else:
            raise EmptyDataFrameException()
            
        # We update the tables DataFrame.
        self.update()
            
    def delete(self, 
               table_name: str):
        """
            Deletes a tables from the system.
        """
        if table_name in [table.name for table in spark.catalog.listTables()]:
            path = self.tables[self.tables.name == table_name].path.reset_index(drop=True)[0]
            sql(f"DROP TABLE IF EXISTS {table_name}")
            dbutils.fs.rm(f'{path}/{table_name}', recurse=True)
            
    def delete_all(self):
        for table_name in self.tables.name.to_list():
            self.delete(table_name)