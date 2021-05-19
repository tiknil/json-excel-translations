#!/usr/local/bin/python3
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
    "-n",
    "--name",
    dest="name",
    help="Name of the excel sheet",
    default="Translations"
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

# Setup variables from arguments
args = parser.parse_args()

def loop_object(base_key, lang_data):
    for key, value in lang_data.items():
        key = f"{base_key}{'.' if base_key != '' else ''}{key}"
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
input_dir = args.input_dir
output_file = args.output_file.strip(' ')
name = args.name

# Get list of translation files in the input folder
cwd = os.getcwd()
os.chdir(input_dir)
files = os.listdir('.')
# Filter out the file not in the locales argument (if provided)
if args.locales != '*':
    locales = args.locales.split(',')
    validFiles = []
    for locale in locales:
        if f"{locale}.json" in files:
            validFiles.append(f"{locale}.json")

    files = validFiles

# Array of languages
langs = []
for file in files:
    splitted = file.split('.')
    if len(splitted) >= 2 and splitted[1] == 'json':
        langs.append(splitted[0])

# Setup global variables that will be populated by the algorithm
output = []
data_by_lang = {}

# Load in memory the json values for all selected langs
for lang in langs:
    inFile = open(f'{input_dir}/{lang}.json', 'r')
    json_data = inFile.read()

    data_by_lang[lang] = json.loads(json_data)
    inFile.close()

# Select the primary language as the language to cycle on
base_data = data_by_lang[primary]


# Recursive function to cycle through the json and extract the values in all the languages
def loop_object(base_key, lang_data):
    for key, value in lang_data.items():
        key = f"{base_key}{'.' if base_key is not '' else ''}{key}"
        if type(value) is dict:
            loop_object(key, value)

        elif type(value) is str:
            # Controllo la presenza nelle altre lingue
            key_translations = []
            for lang_code in langs:
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


# Start recursion
loop_object("", base_data)

# Create the panda dataframe with the data
df = pd.DataFrame(output, columns=(['key'] + langs))
# Create the excel file
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
df.to_excel(writer, index=False, sheet_name=name)

# Excel styling
worksheet = writer.sheets[name]
workbook = writer.book

# Format shared across ALL Cells
defaultFormat = workbook.add_format({'text_wrap': True})

# Set the default format to all cells
for idx, col in enumerate(df):
    worksheet.set_column(idx, idx, 50, defaultFormat)

# Format header
headerFormat = workbook.add_format({'text_wrap': True, 'fg_color': '#DDDDDD', 'border_color': '#333333', 'border': 1, 'align': 'center', 'valign': 'middle', 'bold': True})
worksheet.set_row(0, 20, headerFormat)

# Format key column
keyFormat = workbook.add_format({'text_wrap': True, 'fg_color': '#EEEEEE', 'border_color': '#AAAAAA', 'border': 1})
worksheet.set_column('A:A', 30, keyFormat)

# Format missing values in the value cells (not header and not key)
interval = f"B1:{chr(65+len(langs))}{len(output)}"
missingFormat = workbook.add_format({'text_wrap': True, 'bg_color': '#FFF8DC', 'border_color': '#CCCCCC', 'border': 1})
worksheet.conditional_format(interval, {
    'type': 'cell',
    'criteria': '==',
    'value': '""',
    'format': missingFormat
})

# Lock scrolling on header and keys column
worksheet.freeze_panes(1,1)
writer.save()
