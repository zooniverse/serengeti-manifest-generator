#!/usr/bin/env python
import csv
import json
import sys

if len(sys.argv) != 4:
    print "Usage: python gen_manifest.py FILELIST SEASON OUTPUT"
    sys.exit(1)

_, INPUT_FILELIST, SEASON, OUTPUT = sys.argv

subjects = {}

with open(INPUT_FILELIST) as metadata_f:
    metadata_r = csv.reader(metadata_f)
    metadata_r.next()

    for (season, site, roll, capture, image, path, newtime, oldtime, invalid,
         include) in metadata_r:
        if include != "1":
            continue

        subject_key = "%s-%s-%s" % (site, roll, capture)
        subject = subjects.setdefault(subject_key, {
            'type': 'subject',
            'coords': [],
            'location': [],
            'group': SEASON,
            'metadata': {
                'filenames': [],
                'site_roll_code': '%s_%s_%s' % (season, site, roll),
                'timestamps': [],
            },
        })

        subject['metadata']['filenames'].append(path.split('/')[-1])
        subject['metadata']['timestamps'].append(newtime)
        subject['location'].append(
            'http://s3.amazonaws.com/zooniverse-data/project_data/serengeti/%s' % path
        )

json_out = [
    {
        'type': 'group',
        'name': SEASON,
        'categories': [],
        'metadata': {},
    },
]

json_out += subjects.values()

with open(OUTPUT, 'w') as manifest_f:
    json.dump(json_out, manifest_f)
