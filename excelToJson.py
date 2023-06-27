#!/usr/bin/env python3
import json
from argparse import ArgumentParser

import pandas as pd

parser = ArgumentParser(description='Generate JSON files from the excel.')

parser.add_argument(
    "-k",
    "--key-name",
    dest="key_name",
    help="Name of the Excel column storing the keys (default: '%(default)s') ",
    default="key"
)

parser.add_argument(
    "-i",
    "--input-file",
    dest="input_file",
    help="Name of the input file (default '%(default)s')",
    default="output/translations.xlsx"
)

parser.add_argument(
    "-o",
    "--output-dir",
    dest="output_dir",
    help="Dir where the output files will be written (default '%(default)s')",
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
    help="Size of the output Json indentation (default %(default)s)",
    type=int,
    default=4
)

parser.add_argument(
    "-fk",
    "--flat-keys",
    dest="split_steps",
    help="Set this flag if you want to keep composite keys in your output Json (default is to split composite keys by .)",
    action="store_false",
)

args = parser.parse_args()

file = args.input_file
key_field = args.key_name
output_dir = args.output_dir
empty_flag = args.empty_flag
split_steps = args.split_steps

xl = pd.ExcelFile(file)
df = xl.parse().fillna('')

data = df.values.tolist()

langs = list(df)
langs.remove(key_field)  # Elimino header "key" che non è un linguaggio

lang_translations = {}

for lang in langs:
    lang_translations[lang] = {}


for index, row in df.iterrows():
    key = row[key_field].strip()

    steps = key.split('.') if split_steps else (key,)

    for lang in langs:
        lang_trans = lang_translations[lang]

        for idx, step in enumerate(steps):
            if step not in lang_trans and idx != len(steps) - 1:
                lang_trans[step] = {}
                lang_trans = lang_trans[step]
            elif idx != len(steps) - 1:
                lang_trans = lang_trans[step]

        if empty_flag or row[lang]:
            if not isinstance(lang_trans, str):
                lang_trans[steps[-1]] = row[lang].strip()

for lang in langs:
    out_file = open(f"{output_dir}/{lang}.json", 'w')
    json.dump(lang_translations[lang], out_file, indent=args.indent_size, ensure_ascii=False)
    out_file.close()
