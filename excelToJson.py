#!/usr/local/bin/python3
import json
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser(description='Generate JSON files from the excel.')

parser.add_argument(
    "-k",
    "--key-name",
    dest="key_name",
    help="Name of the Excel column storing the keys (default: 'key') ",
    default="key"
)

parser.add_argument(
    "-i",
    "--input-file",
    dest="input_file",
    help="Name of the input file (default 'output/translations.xlsx')",
    default="output/translations.xlsx"
)

parser.add_argument(
    "-o",
    "--output-dir",
    dest="output_dir",
    help="Dir where the output files will be written (default 'output/')",
    default="output/"
)

parser.add_argument(
    "-e",
    "--empty",
    dest="empty_flag",
    help="Set this flag if you want to include the empty values in your output Json (default is not including the key)",
    action="store_true"
)

parser.add_argument(
    "-is",
    "--indent-size",
    dest="indent_size",
    help="Size of the output Json indentation (default 4)",
    default=4
)

args = parser.parse_args()

file = args.input_file
key_field = args.key_name
output_dir = args.output_dir

xl = pd.ExcelFile(file)
df = xl.parse().fillna('')

data = df.values.tolist()

langs = list(df)
langs.remove(key_field)  # Elimino header "key" che non è un linguaggio

lang_translations = {}

for lang in langs:
    lang_translations[lang] = {}


for index, row in df.iterrows():
    key = row['key']

    steps = key.split('.')

    for lang in langs:
        lang_trans = lang_translations[lang]

        for idx, step in enumerate(steps):
            if step not in lang_trans and idx != len(steps)-1:
                lang_trans[step] = {}
                lang_trans = lang_trans[step]
            elif idx != len(steps)-1:
                lang_trans = lang_trans[step]

        if args.empty_flag or row[lang] != '':
            if not isinstance(lang_trans, str):
                lang_trans[steps[-1]] = row[lang].rstrip()

for lang in langs:
    out_file = open(f"{output_dir}/{lang}.json", 'w')
    json.dump(lang_translations[lang], out_file, indent=args.indent_size, ensure_ascii=False)
    out_file.close()



