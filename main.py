import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
import http.server
import socketserver
import webbrowser
import yaml
import sys
import os


# encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# congigs from yaml
with open('C:/Users/athoo/PIFSS/data-quality/config/rule.yaml', 'r') as rule:
    custom_config = yaml.safe_load(rule)


# loading dataset
df = pd.read_csv(r'C:/Users/athoo/PIFSS/data-quality/inputs/BankChurners.csv')
print(df.columns)

# this part making the data profiling to the original dataframe


# make profile report for the original df
# the only allowed params in ProfileReport are df name and title of the html page
original_report = ProfileReport(df, title="Profiling Report")
original_report.to_widgets()  # this is mostly used for jupetr note
original_report.to_notebook_iframe()

# generate the report of the original df
original_report.to_file(
    r'C:/Users/athoo/PIFSS/data-quality/outputs/profile-report.html')


# this part is for the transformed dataframe( appling the rules to it)


# make the comparisone between the original and the transformed df
# 1- make a copy of the original df
df_trans = df.copy()

# applying custom validation rules based on rule.yaml file
# 2- appy the rules to the df_trans
for rule_entry in custom_config['rule']:
    column = rule_entry['column']
    if 'range' in rule_entry:
        min_range, max_range = rule_entry['range']
        df_trans = df_trans[(df_trans[column] >= min_range)
                            & (df_trans[column] <= max_range)]
    if 'string_length' in rule_entry:
        min_length, max_length = rule_entry['string_length']
        df_trans = df_trans[df_trans[column].str.len().between(
            min_length, max_length)]

# generate the html report for the df_trans
trans_report = ProfileReport(df_trans, title='Transformed Data')
comparison_report = original_report.compare(trans_report)
comparison_report.to_file(
    r'C:/Users/athoo/PIFSS/data-quality/outputs/original-vs-trans.html')


# Specify the directory where the HTML report is located
html_report_directory = r'C:/Users/athoo/PIFSS/data-quality/outputs/'


# Set up a local web server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

# Open the web browser to view the report
webbrowser.open(f'http://localhost:8000/outputs/original-vs-trans.html')

# Start the local web server
print(f"Serving at port 8000")
httpd.serve_forever()
