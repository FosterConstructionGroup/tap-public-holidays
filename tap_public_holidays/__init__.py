import os
import json
import singer
from singer import metadata

from tap_public_holidays.utility import get_abs_path
from tap_public_holidays.fetch import handle_holidays

logger = singer.get_logger()

REQUIRED_CONFIG_KEYS = ["start_year", "end_year"]


def load_schemas():
    schemas = {}

    for filename in os.listdir(get_abs_path("schemas")):
        path = get_abs_path("schemas") + "/" + filename
        file_raw = filename.replace(".json", "")
        with open(path) as file:
            schemas[file_raw] = json.load(file)

    return schemas


def populate_metadata(schema_name, schema):
    mdata = metadata.new()
    mdata = metadata.write(mdata, (), "table-key-properties", ["id"])

    for field_name in schema["properties"].keys():
        mdata = metadata.write(
            mdata,
            ("properties", field_name),
            "inclusion",
            "automatic" if field_name == "id" else "available",
        )

    return mdata


def get_catalog():
    raw_schemas = load_schemas()
    streams = []

    for schema_name, schema in raw_schemas.items():

        # get metadata for each field
        mdata = populate_metadata(schema_name, schema)

        # create and add catalog entry
        catalog_entry = {
            "stream": schema_name,
            "tap_stream_id": schema_name,
            "schema": schema,
            "metadata": metadata.to_list(mdata),
            "key_properties": ["id"],
        }
        streams.append(catalog_entry)

    return {"streams": streams}


def do_discover():
    catalog = get_catalog()
    # dump catalog
    print(json.dumps(catalog, indent=2))


def get_selected_streams(catalog):
    """
    Gets selected streams.  Checks schema's 'selected'
    first -- and then checks metadata, looking for an empty
    breadcrumb and mdata with a 'selected' entry
    """
    selected_streams = []
    for stream in catalog["streams"]:
        stream_metadata = stream["metadata"]
        if stream["schema"].get("selected", False):
            selected_streams.append(stream["tap_stream_id"])
        else:
            for entry in stream_metadata:
                # stream metadata will have empty breadcrumb
                if not entry["breadcrumb"] and entry["metadata"].get("selected", None):
                    selected_streams.append(stream["tap_stream_id"])

    return selected_streams


def get_stream_from_catalog(stream_id, catalog):
    for stream in catalog["streams"]:
        if stream["tap_stream_id"] == stream_id:
            return stream
    return None


def do_sync(config, state, catalog):
    selected_stream_ids = get_selected_streams(catalog)

    # pipelinewise-target-redshift fails without this initial state message, per https://github.com/transferwise/pipelinewise-target-redshift/issues/69
    singer.write_state(state)

    streams_lookup = {stream["tap_stream_id"]: stream for stream in catalog["streams"]}

    if "holidays" in selected_stream_ids:
        d = streams_lookup["holidays"]
        singer.write_schema("holidays", d["schema"], d["key_properties"])

        schemas = {"holidays": d["schema"]}

        state = handle_holidays(config, schemas, state, d["metadata"])

    singer.write_state(state)


@singer.utils.handle_top_exception(logger)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.discover:
        do_discover()
    else:
        catalog = args.properties if args.properties else get_catalog()
        do_sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
