""" This script generates the visualizations JSON object that you can import into Kibana to visualize Cuckoo data"""


import json
from copy import deepcopy

visualize_base = {
    "_id": "Cuckoo-Summary-Directory-Created",
    "_type": "visualization",
    "_source": {
      "title": "Cuckoo - Summary - Directory Created",
      "visState": "{\"title\":\"Cuckoo - Summary - Directory Enumerated\",\"type\":\"table\",\"params\":{\"perPage\":50,\"showPartialRows\":false,\"showMeticsAtAllLevels\":false},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{}},{\"id\":\"2\",\"type\":\"terms\",\"schema\":\"bucket\",\"params\":{\"field\":\"summary.directory_created\",\"size\":50,\"order\":\"desc\",\"orderBy\":\"1\"}}],\"listeners\":{}}",
      "uiStateJSON": "{}",
      "description": "",
      "version": 1,
      "kibanaSavedObjectMeta": {
        "searchSourceJSON": "{\"index\":\"cuckoo*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
      }
    }
  }

visState = {
  "params": {
    "perPage": 50,
    "showMeticsAtAllLevels": False,
    "showPartialRows": False
  },
  "listeners": {},
  "type": "table",
  "aggs": [
    {
      "params": {},
      "type": "count",
      "id": "1",
      "schema": "metric"
    },
    {
      "params": {
        "orderBy": "1",
        "field": "summary.directory_created",
        "order": "desc",
        "size": 50
      },
      "type": "terms",
      "id": "2",
      "schema": "bucket"
    }
  ],
  "title": "Cuckoo - Summary - Directory Enumerated"
}

base_id = "Cuckoo"

summary = """summary.downloads_file
summary.directory_enumerated
summary.wmi_query
summary.directory_created
summary.file_deleted
summary.file_recreated
summary.fetches_url
summary.file_exists
summary.regkey_deleted
summary.connects_ip
summary.command_line
summary.regkey_read
summary.file_failed
summary.file_opened
summary.guid
summary.mutex
summary.file_created
summary.regkey_written
summary.directory_removed
summary.file_moved
summary.resolves_host
summary.file_read
summary.regkey_opened
summary.file_written
summary.file_copied
summary.dll_loaded
summary.connects_host"""

summary_fields = summary.split()

procmemory_fields = ["procmemory.extracted.urls", "procmemory.extracted.type"]

target = """target.file.yara.strings
target.category
target.file.md5
target.file.yara.meta.description
target.file.sha512
target.file.path
target.file.yara.meta.author
target.file.crc32
target.file.sha1
target.file.name
target.file.sha256
target.file.type
target.file.size
target.file.urls
target.file.ssdeep"""

target_fields = target.split()

all_fields = procmemory_fields + summary_fields + target_fields

visualizations = []

for field in all_fields:
    cuckoo_type, cuckoo_name = field.split(".", 1)
    id = "cuckoo" + " " + cuckoo_type + " " + cuckoo_name
    visstate = visState

    visstate["aggs"][1]["params"]["field"] = field
    visualization = deepcopy(visualize_base)

    visualization["_source"]["visState"] = json.dumps(visstate)
    visualization["_id"] = id
    visualization["_source"]["title"] = "cuckoo" + " - " + cuckoo_type + " - " + cuckoo_name
    print visualization["_source"]["title"]

    visualizations.append(visualization)

with open("dumped_visualizations.json", "wb") as f:
    f.write(json.dumps(visualizations, indent=4))
