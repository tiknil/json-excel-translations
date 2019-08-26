#!/bin/bash

virtualenv venv && source venv/bin/activate && pip install -r requirements.txt

chmod +x link.sh
chmod +x ./excelToJson.py
chmod +x ./jsonToExcel.py