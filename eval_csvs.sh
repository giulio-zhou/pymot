#!/bin/bash

GT=$1
HYP=$2
IOU=$3

python convert_csv_to_json.py $GT gt.json gt
python convert_csv_to_json.py $HYP hyp.json hyp

python pymot.py -a gt.json -b hyp.json -i $IOU
