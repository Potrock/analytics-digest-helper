from dune_client.client import DuneClient
from .queries import get_queries
import os
import pickle
import datetime
import time


def get_query_result(queries, query_name, cluster="medium"):
    query = queries[query_name]

    dune = DuneClient(os.environ["DUNE_API_KEY"])
    attempts = 0
    while attempts < 3:
        try:
            pd = dune.refresh_into_dataframe(query, performance=cluster)
            return pd
        except:
            attempts += 1
            time.sleep(2)  # wait for 2 seconds before trying again
    if attempts == 3:
        raise Exception("Failed to get query result after 3 attempts")
    return None


def load(start_date: str, end_date: str, sol_start_deposits: float, sol_end_deposits: float):
    queries = get_queries(start_date, end_date, sol_start_deposits, sol_end_deposits)
    dfs = {}
    for query_name in queries.keys():
        result = get_query_result(queries, query_name, cluster="large")
        if result is not None:
            dfs[query_name] = result

    # now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    # file_name = f"data/dune_data_{now}.pkl"
    # with open(file_name, "wb") as f:
    #     pickle.dump(dfs, f)

    return dfs

