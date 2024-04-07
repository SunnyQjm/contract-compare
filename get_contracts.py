import time
import os
import json
import psycopg2
from typing import List
from SECRET import *
import psycopg2.pool
from contextlib import contextmanager


class SmartContract:
    def __init__(self, contract_address: str, contract_hash: str, contract_type: str):
        self.contract_address = contract_address
        self.contract_hash = contract_hash
        self.contract_type = contract_type
        self.local_path = None

    def get_local_path(self):
        return self.local_path

    def set_local_path(self, local_path):
        self.local_path = local_path

    def __str__(self):
        return f"SmartContract({self.contract_address}, {self.contract_hash}, {self.contract_type})"


conn_pool = psycopg2.pool.ThreadedConnectionPool(1, 200, user=USER, password=PASSWORD, host=HOST, port=PORT,
                                                 database=DATABASE)


@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = conn_pool.getconn()
        yield connection
    finally:
        if connection:
            conn_pool.putconn(connection)


def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = conn_pool.getconn()
        cursor = connection.cursor()
        yield cursor
        if commit:
            connection.commit()
    finally:
        if cursor:
            cursor.close()
        if connection:
            conn_pool.putconn(connection)


def get_smart_contracts():
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT ContractAddress, ContractHash, ContractType  FROM SmartContract WHERE ContractType='Solidity'")
        return [SmartContract(item[0], item[1], item[2]) for item in cur.fetchall()]


def scan_smart_contract_local_path(smart_contracts: List[SmartContract], target_dir: str):
    origin_dir = "xxx"
    finished_contract_hashes = {}
    for smart_contract in smart_contracts:
        if smart_contract.contract_hash in finished_contract_hashes:
            continue
        finished_contract_hashes[smart_contract.contract_hash] = True
        if not os.path.exists(f"{origin_dir}{smart_contract.contract_address[:2]}"):
            print(f"Can not find contract {smart_contract.contract_address} in local path")
            continue
        local_contract_path = f"{origin_dir}{smart_contract.contract_address[:2]}/main.sol"
        if not os.path.exists(local_contract_path):
            print(f"Can not find contract {smart_contract.contract_address} in local path")
            continue

        # Create target_dir if not exists
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_contract_path = f"{target_dir}/{smart_contract.contract_hash}.sol"
        os.system(f"cp {local_contract_path} {target_contract_path}")


if __name__ == '__main__':
    smart_contracts = get_smart_contracts()
    scan_smart_contract_local_path(smart_contracts, "contracts")
