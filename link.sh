#!/bin/bash
BASEDIR=$(dirname $(realpath "$0"))

sudo ln -s $BASEDIR/excelToJson.py /usr/local/bin/excelToJson
sudo ln -s $BASEDIR/jsonToExcel.py /usr/local/bin/jsonToExcel