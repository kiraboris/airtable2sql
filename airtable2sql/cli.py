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


def fetch_base_metadata(base_id, token):
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tables for base {base_id}: {response.status_code} {response.text}")
    return response.json()["tables"]


def get_all_bases(token):
    url = "https://api.airtable.com/v0/meta/bases"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch base list: {response.status_code} {response.text}")
    return response.json()["bases"]


def export_base_to_sqlite(base_id, base_name, output_dir, token):
    print(f"\n📦 Exporting base: {base_name} ({base_id})")

    tables_meta = fetch_base_metadata(base_id, token)
    api = Api(token)

    # Safe file name
    db_name = f"{base_name.replace(' ', '_')}.db"
    db_path = os.path.join(output_dir, db_name)
    engine = create_engine(f"sqlite:///{db_path}")

    for table in tables_meta:
        table_id = table['id']
        table_name = table['name'].replace(" ", "_")
        print(f"  🔄 Processing table: {table_name}")

        table_obj = api.table(base_id, table_id)
        df = airtable_to_df(table_obj)

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"  ✅ Saved table '{table_name}'")

    print(f"✅ Finished exporting '{base_name}' → {db_path}")


def main():
    parser = argparse.ArgumentParser(description="Download Airtable bases and store them in SQLite databases.")
    parser.add_argument("-b", "--base", help="Airtable base ID (if omitted, all accessible bases will be exported)")
    parser.add_argument("-o", "--output", help="Output directory for database files (default: current directory)")
    parser.add_argument("-t", "--token", default=os.environ.get("AIRTABLE_API_KEY"),
                        help="Airtable Personal Access Token (or set AIRTABLE_API_KEY environment variable)")

    args = parser.parse_args()

    if not args.token:
        parser.error("No Airtable token provided. Use --token or set AIRTABLE_API_KEY environment variable.")

    output_dir = args.output or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    if args.base:
        # Single base
        bases = get_all_bases(args.token)
        base_info = next((b for b in bases if b["id"] == args.base), None)
        if not base_info:
            raise Exception(f"Base ID {args.base} not found in your account.")
        export_base_to_sqlite(args.base, base_info["name"], output_dir, args.token)
    else:
        # All bases
        bases = get_all_bases(args.token)
        for base in bases:
            export_base_to_sqlite(base["id"], base["name"], output_dir, args.token)
