import singer
import singer.metrics as metrics
from singer import metadata
from bs4 import BeautifulSoup
from tap_public_holidays.utility import (
    get_data,
    format_date,
)


def handle_holidays(config, schemas, state, mdata):
    extraction_time = singer.utils.now()

    start_year = config["start_year"]
    end_year = config["end_year"]

    # TODO: range
    # TODO: scrape

    html = get_data(start_year)
    soup = BeautifulSoup(html)

    print(soup)

    holidays = []

    # write_many(holidays, "holidays", schemas["holidays"], mdata, extraction_time)

    return write_bookmark(state, "holidays", extraction_time)


# More convenient to use but has to all be held in memory, so use write_record instead for resources with many rows
def write_many(rows, resource, schema, mdata, dt):
    with metrics.record_counter(resource) as counter:
        for row in rows:
            write_record(row, resource, schema, mdata, dt)
            counter.increment()


def write_record(row, resource, schema, mdata, dt):
    with singer.Transformer() as transformer:
        rec = transformer.transform(row, schema, metadata=metadata.to_map(mdata))
    singer.write_record(resource, rec, time_extracted=dt)


def write_bookmark(state, resource, dt):
    singer.write_bookmark(state, resource, "since", format_date(dt))
    return state
