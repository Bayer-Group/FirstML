import os
import json
import pandas as pd
import snowflake.connector
from dotenv import find_dotenv, load_dotenv


class SnowflakeConn:
    def __init__(self):
        print("init snowflake session")

        # find .env automagically by walking up directories until it's found
        dotenv_path = find_dotenv()

        # load up the entries as environment variables
        load_dotenv(dotenv_path)
        
        if os.environ.get("SNOWFLAKE_PWD") is not None:
            self.sf_user = os.environ.get("SNOWFLAKE_USER")
            self.sf_pwd = os.environ.get("SNOWFLAKE_PWD")
            self.sf_account = os.environ.get("SNOWFLAKE_ACCOUNT")
            self.sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE")
            self.sf_db = os.environ.get("SNOWFLAKE_DB")
            self.sf_role = os.environ.get("SNOWFLAKE_ROLE")
            self.sf_schema = os.environ.get("SNOWFLAKE_SCHEMA")
            self.sf_auth_mode='password'
        else:
            tokenfile = open(os.environ.get("SNOWFLAKE_TOKEN_PATH"))
            tokendata = json.load(tokenfile)
            token = tokendata["access_token"]
            self.sf_access_token = token
            self.sf_account = os.environ.get("SNOWFLAKE_ACCOUNT")
            self.sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE")
            self.sf_db = os.environ.get("SNOWFLAKE_DB")
            self.sf_role = os.environ.get("SNOWFLAKE_ROLE")
            self.sf_schema = os.environ.get("SNOWFLAKE_SCHEMA")
            self.sf_auth_mode='oauth'

        self.cur = None

        self.session()

    def session(self):
        if self.sf_auth_mode =='password':
            conn = snowflake.connector.connect(
                user=self.sf_user,
                password=self.sf_pwd,
                account=self.sf_account,
                warehouse=self.sf_warehouse,
                database=self.sf_db,
                role=self.sf_role,
                schema=self.sf_schema,
            )
        else:
            conn = snowflake.connector.connect(
              authenticator="OAUTH",
              token = self.sf_access_token,
              account=self.sf_account,
              warehouse=self.sf_warehouse,
              database=self.sf_db,
              role=self.sf_role,
              schema=self.sf_schema,
            )
        
        self.cur = conn.cursor()

    def _query(self, q):
        self.cur.execute(q)
        return pd.DataFrame.from_records(iter(self.cur), columns=[x[0] for x in self.cur.description])

    def query(self, q):
        try:
            return self._query(q)
        except Exception:
            self.session()
            return self._query(q)

    def return_connection(self, db, schema):
        
        if self.sf_auth_mode =='password':
            conn = snowflake.connector.connect(
                user=self.sf_user,
                password=self.sf_pwd,
                account=self.sf_account,
                warehouse=self.sf_warehouse,
                database=self.sf_db,
                role=self.sf_role,
                schema=self.sf_schema,
            )
        else:
            conn = snowflake.connector.connect(
              authenticator="OAUTH",
              token = self.sf_access_token,
              account=self.sf_account,
              warehouse=self.sf_warehouse,
              database=self.sf_db,
              role=self.sf_role,
              schema=self.sf_schema,
            )
            
        return conn
