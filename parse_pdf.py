import datefinder
import functools
import json
import math
import pandas as pd
import os
import re

from pdfminer.high_level import extract_pages
import tabula

def process_file(filepath):
    print(f"[START] Processing district {file} at {file_location}")
    data = extract_pages(filepath)
    data = list(map(lambda x: list(x), data))
    assert len(data) == 6, "Files must have 6 pages exactly - not more, not less."
    ALL_INFO = dict() # all information stored here
    
    '''
        - Page 0 (title page) and page 5 (back cover) do not need processing. 
        
        - Page 1 contains some introductory text, that we just extract. Also, we try to extract
          the start, end dates of fieldwork and (TODO) the n_households, n_women, and n_men samples
        
        - Page 2, 3, 4 contain tables with 
        - 
    '''
    
    # Process Page 1: this just contains some introductory text, so we just extract all the text.
    extracted_texts = list(map(lambda x: x.get_text().replace('\n', ''), data[1])) # get text, remove new lines
    intro = functools.reduce(lambda a, b: a+b, extracted_texts).strip()
    intro = re.sub('\s+',' ', intro)

    ALL_INFO['intro'] = intro

    # attempt to parse dates from this page
    possible_dates = list(datefinder.find_dates(intro, source=True))

    MIN_NUM_CHARS_IN_FULL_DATE = 7 # the shortest date I can think of is "May 1, 2021", so atleast 11 characters. Let's use 7 just to be safe
    possible_dates = list(filter(lambda x: len(x[1]) > MIN_NUM_CHARS_IN_FULL_DATE, possible_dates))
    if len(possible_dates) == 2:
        ALL_INFO['fieldwork_start_date'] = min(possible_dates[0][0], possible_dates[1][0]).isoformat()
        ALL_INFO['fieldwork_end_date'] = max(possible_dates[0][0], possible_dates[1][0]).isoformat()
    
    FIND_STRING = "information was gathered from"
    index = intro.find(FIND_STRING)
    relevant_substring = intro[index:].replace(',', '')
    numbers_in_substring = [int(i) for i in relevant_substring.split() if i.isdigit()]
    if len(numbers_in_substring) == 3:
        households, women, men = numbers_in_substring
        ALL_INFO['n_households'] = households
        ALL_INFO['n_women'] = women
        ALL_INFO['n_men'] = men
    
    tables = tabula.read_pdf(filepath, pages=[3, 4, 5], stream=True)
    assert len(tables) == 3

    table_rows = list(map(lambda x: x.shape[0], tables))
    table_cols = list(map(lambda x: x.shape[1], tables))
    assert(len(set(table_cols))) == 1, "All tables should have same number of columns."

    num_cols = max(table_cols)
    new_col_names = ["Indicator", "NFHS5", "NFHS4"][:num_cols]

    full_table = pd.concat(tables, ignore_index=True)
    col_names = full_table.columns

    full_table = full_table.rename(columns={
        k:v for k, v in zip(col_names, new_col_names)
    })[["Indicator", "NFHS5"]]

    full_table = full_table.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    full_table = full_table[full_table['Indicator'] != 'Indicators'].reset_index(drop=True)
    full_table = full_table[full_table['NFHS5'] != 'Total'].reset_index(drop=True)
    full_table["Indicator"] = full_table["Indicator"].apply(lambda x: x.strip())

    all_headings = pd.read_csv("headings.csv", sep="#")
    all_headings = all_headings["Headings"].apply(lambda x: x.strip()) 
    full_table = full_table[~full_table['Indicator'].isin(all_headings)].reset_index(drop=True)

    def num_cases(x):
        if x == "*":
            return "Percentage not shown; based on fewer than 25 unweighted cases"
        try:
            y = float(x)
            return None
        except:
            if '(' in x and ')' in x:
                return "Based on 25-49 unweighted cases"

    def process(x):
        if x == '*':
            return math.nan
        if type(x) == float:
            return x
        else:
            x = x.replace(',', '').replace(')', '').replace('(', '') # make sure to remove numbers 
            return float(x)

    full_table['num_cases'] = full_table['NFHS5'].apply(num_cases)
    full_table['NFHS5'] = full_table['NFHS5'].apply(process)

    full_table["temp"] = full_table["Indicator"].apply(lambda x: not x.split('.')[0].strip().isdigit())

    for index, row in full_table[full_table['temp']].iterrows():
        full_table.loc[index-1, 'NFHS5'] = row['NFHS5']
        full_table.loc[index-1, 'Indicator'] += f" {row['Indicator']}"

    full_table = full_table[~full_table['temp']]
    full_table = full_table[["Indicator", "NFHS5", "num_cases"]].reset_index(drop=True)
    full_table['IndicatorNumber'] = full_table['Indicator'].apply(lambda x: int(x.split('.')[0]))
    full_table['Indicator'] = full_table['Indicator'].apply(lambda x: (x.split('.')[1]))
    full_table = full_table[['IndicatorNumber', 'Indicator', 'NFHS5', 'num_cases']]
    
    values_dict = dict()
    for index, row in full_table.iterrows():
        tmp = dict()
        tmp['indicator'] = row['Indicator']
        tmp['value'] = row['NFHS5']
        if row['num_cases'] is not None:
            tmp['info'] = row['num_cases']
        values_dict[row['IndicatorNumber']] = tmp
    
    ALL_INFO['indicators'] = values_dict
    
    filepath_to_save = f'{filepath}.json'
    assert not os.path.exists(filepath_to_save), "This program shall not overwrite files."
    with open(filepath_to_save, 'w') as f:
        json.dump(ALL_INFO, f)
    print(f"[END] Saved JSON to {filepath_to_save}")

for root, dirs, files in os.walk(os.path.abspath("data")):
    for file in files:
        file_location = os.path.join(root, file)
        process_file(file_location)