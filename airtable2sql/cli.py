import os
import json
import requests
import pandas as pd
from pyairtable import Api
from sqlalchemy import create_engine
import argparse


def sanitize_field(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return value


def airtable_to_df(table_obj):
    records = table_obj.all()
    data = []
    for record in records:
        fields = record['fields']
        clean_fields = {k: sanitize_field(v) for k, v in fields.items()}
        clean_fields['_id'] = record['id']
        data.append(clean_fields)
    return pd.DataFrame(data)


def main(base_id, output_db, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 1: Get metadata for all tables in base
    meta_url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    response = requests.get(meta_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch tables: {response.status_code} {response.text}")

    tables_meta = response.json()["tables"]

    # Step 2: Init Airtable API and SQLite engine
    api = Api(token)
    engine = create_engine(f'sqlite:///{output_db}')

    # Step 3: Download and store each table
    for table in tables_meta:
        table_id = table['id']
        table_name = table['name'].replace(" ", "_")
        print(f"🔄 Processing table: {table_name} ({table_id})")

        table_obj = api.table(base_id, table_id)
        df = airtable_to_df(table_obj)

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Saved '{table_name}' to {output_db}")


def cli():
    parser = argparse.ArgumentParser(description="Download all Airtable tables and store them in a SQLite DB.")
    parser.add_argument("-b", "--base", required=True, help="Airtable base ID (e.g. appXXXXXXXXXXXXXX)")
    parser.add_argument("-o", "--output", required=True, help="Path to output SQLite database file")
    parser.add_argument("-t", "--token", default=os.environ.get("AIRTABLE_API_KEY"),
                        help="Airtable Personal Access Token (can use AIRTABLE_API_KEY env variable)")

    args = parser.parse_args()

    if not args.token:
        parser.error("No Airtable token provided. Use --token or set AIRTABLE_API_KEY environment variable.")

    main(args.base, args.output, args.token)


if __name__ == "__main__":
    cli()
