# airtable2sql
Easily export **Airtable** bases to **SQLite** databases.

Useful for:

- Sharing data
- Storing local backups

## Installation

You can install **airtable2sql** using pip directly from this github repository.

```sh
pip install git+https://github.com/alberdilab/airtable2sql.git
```

## Access token

You need a personal access token in order to be able to fetch Airtable data programatically.

> https://airtable.com/create/tokens

Make sure that the token has access to all the bases you want to export, and that the following Scopes are selected:

- data.records:read
- schema.bases:read
- workspaceAndBases:read

Store the token in a safe place, and use it in airtable2sql either through the -t argument, or by exporting the AIRTABLE_API_KEY variable before using airtable2sql.

```sh
export AIRTABLE_API_KEY="HEREISYOURTOKEN"
```

```sh
airtable2sql -t HEREISYOURTOKEN
```

## Usage

You need a personal access token in order to be able to fetch Airtable data programatically.

### Export all bases

If no arguments are given, airtable2sql will export all the bases that can be fetched using the provided personal access token, and create a sqlite database for each of them in the working directory.

```sh
airtable2sql
```

### Export desired bases

You can select one or multiple bases to be exported using the -b argument.

```sh
airtable2sql -b appHrXl9ANV7Q8STF,appKakM1bnHEekwuW
```

### Export to another directory

By default, airtable2sql will export the databases to the working directory, unless another existing directory is provided using the -o argument.

```sh
airtable2sql -b appHrXl9ANV7Q8STF,appKakM1bnHEekwuW -o home/airtable_backup
```
