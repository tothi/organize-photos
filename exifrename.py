#!/usr/bin/env python3
#
# batch rename files according to exif date/time & camera model
#

from pathlib import Path
import sys
import exiftool
import json
import re
import os
from datetime import datetime
from datetime import timedelta
from dateutil import parser as dtparser

CONFIG = "exifrename.conf"

# DATETIME_EXIF = ['EXIF:CreateDate', 'H264:DateTimeOriginal', 'File:FileModifyDate', 'QuickTime:MediaCreateDate']
DATETIME_EXIF = ['EXIF:CreateDate', 'H264:DateTimeOriginal', 'File:FileModifyDate']
MODEL_EXIF = ['EXIF:Model', 'H264:Model', 'QuickTime:ComAndroidModel']

def extractModel(metadata):
    for mk in MODEL_EXIF:
        if mk in metadata:
            return metadata[mk]
    return None

def extractDate(metadata):
    for dk in DATETIME_EXIF:
        if dk in metadata:
            return dtparser.parse(re.sub(r' [A-Z]{3}$', '', re.sub(':', '-', metadata[dk], 2)))
    return None

def translateModel(model):
    return conf_model[model]['ext']

def translateDate(d, model):
    if 'deltamins' in conf_model[model]:
        d = d + timedelta(minutes=int(conf_model[model]['deltamins']))
    return d.strftime("%Y%m%d_%H%M%S")

def safeFileName(filename):
    i = 1
    fp = Path(filename)
    filename2 = filename
    while os.path.exists(filename2):
        filename2 = '%s/%s_%d%s' % (str(fp.parent), str(fp.stem), i, str(fp.suffix))
        i += 1
    return filename2

with open(CONFIG, 'r') as conf_file:
    conf = json.load(conf_file)
    conf_model = {}
    for dev in conf['devices']:
        conf_model[dev['model']] = dev
    print("[+] config file %s parsed" % CONFIG)

pathlist = Path(sys.argv[1]).glob('**/*.*')
for path in pathlist:
    f = str(path)
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(f)
        # print(metadata)
        model = extractModel(metadata)
        createdate = extractDate(metadata)
        if (model is None) or (createdate is None):
            print("[-] Cannot get Model info or CreateDate: file %s seems to be not a proper media file, skipping." % f)
            continue
        model2 = translateModel(model)
        createdate2 = translateDate(createdate, model)
        parent = str(path.parent)
        suffix = path.suffix.lower()
        newname = parent+'/'+createdate2+'_'+model2+suffix
        f1 = safeFileName(newname)
        os.rename(f, f1)
        print("[+] %s -> %s" % (f, f1))
