import json

import yaml
import pathlib
import s3fs
import environ

env = environ.Env()

S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
S3_BUCKET = env("S3_BUCKET")
S3_PATH = env("S3_PATH", default="/geoapi/*.json")

base_config = yaml.load(pathlib.Path("base.yml").open(), yaml.SafeLoader)

s3 = s3fs.S3FileSystem(anon=True, endpoint_url=S3_ENDPOINT_URL)

resources = {}

resource_files = s3.glob(f"{S3_BUCKET}{S3_PATH}")

for resource_file in resource_files:
    for resource in json.loads(s3.open(resource_file).read()):
        resources[resource["id"]] = resource


base_config["resources"] = resources

yaml.dump(base_config, pathlib.Path("local.config.yml").open("w"), yaml.SafeDumper)
