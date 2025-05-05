import json

import yaml
import pathlib
import s3fs

base_config = yaml.load(pathlib.Path("base.yml").open(), yaml.SafeLoader)

s3 = s3fs.S3FileSystem(anon=True, endpoint_url="https://s3-int-1.nina.no")

resources = {}

resource_files = s3.glob("miljodata-test/geoapi/*.json")

for resource_file in resource_files:
    for resource in json.loads(s3.open(resource_file).read()):
        resources[resource["id"]] = resource


base_config["resources"] = resources

yaml.dump(base_config, pathlib.Path("local.config.yml").open("w"), yaml.SafeDumper)
