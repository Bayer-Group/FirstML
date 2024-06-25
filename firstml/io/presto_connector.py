import os

import pandas as pd
import prestodb
from dotenv import find_dotenv, load_dotenv
from oauth_keys2 import get_keys


class PrestoConn:
    def __init__(self):
        print("init presto session")

        # find .env automagically by walking up directories until it's found
        dotenv_path = find_dotenv()

        # load up the entries as environment variables
        load_dotenv(dotenv_path)

        self.pr_api_key = os.environ.get("PRESTO_API_KEY")
        self.pr_api_url = os.environ.get("PRESTO_API_URL")
        self.pr_host = os.environ.get("PRESTO_HOST")
        self.pr_schema = os.environ.get("PRESTO_SCHEMA")

        self.cur = None

        self.session()

    def session(self):
        resp = get_keys(
            target="emr?no_cache",
            api_key=self.pr_api_key,
            api_url=self.pr_api_url,
        )
        print("resp:", resp)
        creds = resp["session"]

        conn = prestodb.dbapi.connect(
            host=self.pr_host,
            port=443,
            catalog="hive",
            schema=self.pr_schema,
            http_scheme="https",
            auth=prestodb.auth.BasicAuthentication(creds["username"], creds["password"]),
        )

        self.cur = conn.cursor()

    def _query(self, q):
        self.cur.execute(q)
        return pd.DataFrame(self.cur.fetchall(), columns=[x[0] for x in self.cur.description])

    def query(self, q):
        try:
            return self._query(q)
        except Exception:
            self.session()
            return self._query(q)
