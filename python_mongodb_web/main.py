import urllib.request
import json
from typing import Any, Dict, List


import flask
from pymongo import MongoClient


JSON_URL = (
    "https://ics.multieditoras.com.br/ics/agenda/1/2017/12?chave=TFACS-PD6L7-WG5ZF-Q9WU9&cliente=10378405"
    "&compacto=0&formato=json"
)


def get_json_file():
    with urllib.request.urlopen(JSON_URL) as url:
        json_content = json.loads(url.read())
        return json_content['agenda']


def save_to_mongodb(conn: MongoClient, db: str, table: str, agendas: List[Dict[str, Any]]):
    agenda_table = eval(f"conn.{db}.{table}")
    agenda = agendas[0]
    item = {
        "id": int(agenda['@id']),
        "nome": agenda['nome'],
        "esfera": agenda['esfera']
    }
    agenda_table.insert_one(item)
    print("Record successfully inserted")


def read_from_mongodb(conn: MongoClient, db: str, table: str):
    return eval(f"conn.{db}.{table}.find()")


def create_website(records):
    rafa_website = flask.Flask('Rafa Website')

    with rafa_website.app_context():
        rendered = flask.render_template('index.html', title="Rafa Website", rows=records)

    with open('rafa.html', 'w') as html_file:
        html_file.write(rendered)
        html_file.close()


if __name__ == "__main__":
    agendas = get_json_file()
    conn = MongoClient('localhost')  # Default port is 27017
    db_name = 'rafa_db'
    table_name = 'agenda'
    save_to_mongodb(conn, db_name, table_name, agendas)
    records = read_from_mongodb(conn, db_name, table_name)
    create_website(records)