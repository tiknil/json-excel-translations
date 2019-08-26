# Localize Json

Two python script to convert JSON translation files to excel and the other way around. It has been created to work with [I18n](https://github.com/mashpie/i18n-node).

The character used of object nesting in json is the dot `.`

The following json structure:
```json
{
  "app": {
    "name": "App Name"
  }
}
```
Produces a key named `app.name`

## Installation

Clone the project:

```bash
git clone https://github.com/tiknil/json-excel-translations.git
cd json-excel-translations
```

Setup the virtualenv with the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

Now you can use the script:
```bash
./jsonToExcel.py -o output/file -i input/folder
./exceltoJson.py -i input/file -o output/folder
```

You can use the link script to setup the scripts in your `/usr/local/bin` folder, so they can be used from everywhere:

```bash
sudo ./link.sh
jsonToExcel -o output/file -i input/folder
exceltoJson -i input/file -o output/folder
``` 

## Usage


### jsonToExcel
The scripts assumes a folder of `.json` files named after their respective locale: `it.json`, `en.json`, ...

It creates an excel file where each column represents a locale and each row is a translation key.


The key are obtained from the primary language (default `en`, it can be configured using the `-p` argument)

Assume we have a folder, named `translations`, with 2 files: `it.json` and `en.json`, where the primary language is `it`.

Given the command:
```
jsonToExcel.py -o translations.xlsx -i translations -p it
```

It produces an excel file named translations.xlsx structured as:

| **key**  | **it**  | **en**   |
|---|---|---|
| keyName  | italiano  | inglese  |

#### Options
- `-h` Instructions on the script usage 
- `-o`/`--output-file` where the excel file must be created (default `output/translations.xlsx`)
- `-i`/`--input-dir` where the translation files are located (default `translations/`)
- `-p`/`--primary` where the excel file must be created (default `en`)
- `-l`/`--locales` A comma-separated list of the locales to select (default all json files in the input directory)


### excelToJson


Given an excel files structured as in the table below

| **key**  | **locale1**  | **locale2**   |
|---|---|---|
| keyName  | locale1 string  | locale2 string  |
| keyName2  | ...  | ...  |

It produces a json file for each locale containing the corresponding translations.

#### Options
- `-h` Instructions on the script usage 
- `-o`/`--output-dir` outpit directory for the translation files (default `translations/`)
- `-i`/`--input-file` location of the excel input file (default `output/translations.xlsx`)
- `-e`/`--empty` set this flag to also include keys without a translation (default is to NOT include keys without a translation, assuming there is a fallback mechanism in your app for such strings)
- `-k`/`--key-name` name of the excel column containing the keys (default `key`)
- `-id`/`--indent-size` size of the Json indentation (default is `4`)