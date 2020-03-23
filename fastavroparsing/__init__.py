import json
import glob
from fastavro import parse_schema
from gcloudlogging.logger import create_logger

log = create_logger()
fastavro_mappings = {}

schema_files = glob.glob('fhir-fastavro/schema/*.avsc')
schema_files.sort()

for schema_file in schema_files:
    with open(schema_file, 'r') as f:
        schema_json = json.load(f)

        try:
            schema = parse_schema(schema_json)
            if 'name' in schema_json:
                resource_type = schema_json["name"]
                log.info(f'Adding schema for {resource_type}')
                fastavro_mappings[resource_type] = schema
        except Exception as e:
            log.error(e)
            continue


def get_fastavro_schema(resource_type):
    return fastavro_mappings[resource_type]


def get_bundle_schema():
    return fastavro_mappings['Bundle']
