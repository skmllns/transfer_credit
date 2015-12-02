import csv
import re

header = ['Transfer Institution', 'Transfer Crs', 'Title', 'BU Equiv Crs', 'Catalog Year']

# strip empty lines (from SO)
with open("Transfer Credit Report by Institution.txt") as trans_file:
    lines = (line.rstrip() for line in trans_file)
    lines = list(line for line in lines if line)

inst_patt_regex = re.compile(r'(?<=Transfer Institution:).*')

file_name = raw_input("Please enter the file name: ")
inf = open(file_name, 'wb')
crs_writer = csv.writer(inf)
crs_writer.writerow(header)

for idx, line in enumerate(lines):
    if inst_patt_regex.search(line):
        inst = inst_patt_regex.search(line).group(0).strip()    # institution name and id
    if '------------' in line:
        idx += 1
        line = lines[idx]
        while 'Bellarmine University' not in line:
            line_results = []
            line_results.append(inst)
            line = line.lstrip()

            line_results.append(line[0:14].rstrip())            # transfer course
            line_results.append(line[14:46].rstrip())           # transfer course title
            line_results.append(line[46:58].rstrip())           # BU equiv course
            line_results.append(line[58:62].rstrip())           # catalog year

            crs_writer.writerow(line_results)

            if idx + 1 < len(lines):
                idx += 1
                line = lines[idx]
            else:
                break

inf.close()
