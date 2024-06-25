from firstml.io.presto_connector import PrestoConn

# credentials are read from .env file,
# same file has been copied to ~/s3result/nodebooks/nodebook_runs/USER/
# in case of re-running experiment in the result folder
from firstml.io.snowflake_connector import SnowflakeConn


class Connector:
    def __init__(self, conn_str):

        if conn_str == "snowflake":
            self.conn = SnowflakeConn()
        elif conn_str == "presto":
            self.conn = PrestoConn()
        else:
            print("choose snowflake or presto")
