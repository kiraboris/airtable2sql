# airtable2sql
Software to export airtable bases into sql databases

```sh
pip uninstall airtable2sql -y
pip install git+https://github.com/alberdilab/airtable2sql.git
airtable2sql -h

airtable2sql -b appHrXl9ANW6Q8STF -o test.db



curl -X GET \
  https://api.airtable.com/v0/meta/bases \
  -H "Authorization: Bearer YOUR_API_KEY"

```
