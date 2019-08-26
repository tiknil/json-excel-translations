#!venv/bin/python3
import json
import os
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser(description='Create an Excel file from a list of json translation files.')

parser.add_argument(
    "-p",
    "--primary",
    dest="primary",
    help="Primary lang (default 'en')",
    default="en"
)

parser.add_argument(
    "-i",
    "--input-dir",
    dest="input_dir",
    help="Dir of the json files",
    default="translations/"
)

parser.add_argument(
    "-l",
    "--locales",
    dest="locales",
    help="(Optional) Comma separated list of the locales to consider (es. it,en,de,fr..)",
    default="*"
)

parser.add_argument(
    "-o",
    "--output-file",
    dest="output_file",
    help="Name of the output file",
    default="output/translations.xlsx"
)

args = parser.parse_args()


def loop_object(base_key, lang_data):
    for key, value in lang_data.items():
        key = f"{base_key}{'.' if base_key is not '' else ''}{key}"
        if type(value) is dict:
            loop_object(key, value)

        elif type(value) is str:
            # Controllo la presenza nelle altre lingue
            key_translations = [value]
            for lang_code in langs:
                if lang_code == primary:
                    continue

                lang_translation = ""
                lang_object = data_by_lang[lang_code]
                steps = key.split('.')
                for step in steps:
                    if step in lang_object:
                        lang_object = lang_object[step]
                    else:
                        break
                if type(lang_object) is str:
                    lang_translation = lang_object
                key_translations.append(lang_translation)

            output.append([key] + key_translations)

primary = args.primary

input_dir = args.input_dir.strip(' /')
output_file = args.output_file.strip(' ')


cwd = os.getcwd()
os.chdir(input_dir)
files = os.listdir('.')

if args.locales != '*':
    locales = args.locales.split(',')
    validFiles = []
    for locale in locales:
        if f"{locale}.json" in files:
            validFiles.append(f"{locale}.json")

    files = validFiles

langs = []
for file in files:
    splitted = file.split('.')
    if len(splitted) >= 2 and splitted[1] == 'json':
        langs.append(splitted[0])

os.chdir("../")

output = []

data_by_lang = {}

for lang in langs:
    inFile = open(f'{input_dir}/{lang}.json', 'r')
    json_data = inFile.read()

    data_by_lang[lang] = json.loads(json_data)
    inFile.close()

base_data = data_by_lang[primary]

loop_object("", base_data)

df = pd.DataFrame(output, columns=(['key'] + langs))

writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
df.to_excel(writer, index=False, sheet_name="coffee cApp")

# FORMATTAZIONE EXCEL
worksheet = writer.sheets["coffee cApp"]
workbook = writer.book
defaultFormat = workbook.add_format({'text_wrap': True})

for idx, col in enumerate(df):
    worksheet.set_column(idx, idx, 50, defaultFormat)

# Format header
headerFormat = workbook.add_format({'text_wrap': True, 'fg_color': '#DDDDDD', 'border_color': '#333333', 'border': 1, 'align': 'center', 'valign': 'middle', 'bold': True})
worksheet.set_row(0, 20, headerFormat)

# Format della riga di chiavi
keyFormat = workbook.add_format({'text_wrap': True, 'fg_color': '#EEEEEE', 'border_color': '#AAAAAA', 'border': 1})
worksheet.set_column('A:A', 30, keyFormat)

interval = f"B1:{chr(65+len(langs))}{len(output)}"
missingFormat = workbook.add_format({'text_wrap': True, 'bg_color': '#FFF8DC', 'border_color': '#CCCCCC', 'border': 1})
worksheet.conditional_format(interval, {
    'type': 'cell',
    'criteria': '==',
    'value': '""',
    'format': missingFormat
})

# Blocco l'intestazione e le chiavi
worksheet.freeze_panes(1,1)
writer.save()
