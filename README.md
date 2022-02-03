# tap-public-holidays

This is a [Singer](https://singer.io) tap that produces JSON-formatted
data from the [publicholidays.co.nz site](https://publicholidays.co.nz) following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Scrapes NZ public holidays from the [publicholidays.co.nz site](https://publicholidays.co.nz)
- Extracts the following resources:
  - Daily summary stats by location
  - Hourly detailed data by location
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick start

1. Install

   We recommend using a virtualenv:

   ```bash
   > virtualenv -p python3 venv
   > source venv/bin/activate
   > pip install -e .
   ```

2. Create the config file

   Create a JSON file called `config.json` containing

   - a start year
   - an end year

   ```json
   {
     "start_year": 2020,
     "end_year": 2023
   }
   ```

3. Run the tap in discovery mode to get properties.json file

   ```bash
   tap-public-holidays --config config.json --discover > properties.json
   ```

4. In the properties.json file, select the streams to sync

   Each stream in the properties.json file has a "schema" entry. To select a stream to sync, add `"selected": true` to that stream's "schema" entry. For example, to sync the pull_requests stream:

   ```
   ...
   "tap_stream_id": "holidays",
   "schema": {
     "selected": true,
     "properties": {
   ...
   ```

5. Run the application

   `tap-public-holidays` can be run with:

   ```bash
   tap-public-holidays --config config.json --properties properties.json
   ```
