import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
import http.server
import socketserver
import webbrowser
import yaml
import sys



# encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# congigs from yaml 
with open('C:/Users/athoo/PIFSS/data-quality/config/rule.yaml','r') as rule:
    custom_config = yaml.safe_load(rule)



# loading dataset 
df = pd.read_csv(r'C:/Users/athoo/PIFSS/data-quality/inputs/BankChurners.csv')


# Apply custom validation rules based on the rule.yaml file
for rule_entry in custom_config['rule']:
    column = rule_entry['column']
    if 'range' in rule_entry:
        min_range, max_range = rule_entry['range']
        df = df[(df[column] >= min_range) & (df[column] <= max_range)]
    if 'string_length' in rule_entry:
        min_length, max_length = rule_entry['string_length']
        df = df[df[column].str.len().between(min_length, max_length)]
    


# profile report
profile = ProfileReport(df, title= "Profiling Report") # this function doesn't accept other params than the used 
profile.to_widgets()
profile.to_notebook_iframe()

# generate the report + pass custom_config to Jinja2 template
profile.to_file(r'C:/Users/athoo/PIFSS/data-quality/outputs/profile-report.html')


# Specify the directory where the HTML report is located
html_report_directory = r'C:/Users/athoo/PIFSS/data-quality/outputs/'


# Set up a local web server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

# Open the web browser to view the report
webbrowser.open(f'http://localhost:8000/outputs/profile-report.html')


# Start the local web server
print(f"Serving at port 8000")
httpd.serve_forever()






