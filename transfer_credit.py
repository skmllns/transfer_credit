import csv
import re


def extract_elem(re_obj, rvsd_line, rvsd_results):
    re_result = re_obj.search(rvsd_line)
    if re_result:
        rvsd_results.append(re_result.group(0).lstrip().rstrip())
        rvsd_line = rvsd_line.replace(re_result.group(0), '', 1).lstrip()
    else:
        rvsd_results.append('')
    return rvsd_line, rvsd_results


header = ['Transfer Institution', 'Transfer Crs', 'Title', 'BU Equiv Crs', 'Catalog Year']

# strip empty lines (from SO)
with open("Transfer Credit Report by Institution.txt") as trans_file:
    lines = (line.rstrip() for line in trans_file)
    lines = list(line for line in lines if line)

# define patterns
inst_patt_regex = re.compile(r'(?<=Transfer Institution:).*')
transf_crs_patt_regex = re.compile(r"(([A-Z\d][A-Z\.\-\&\:\d][A-Z\.\-\&\:\d]*)*\s*\-*\:*\s*\d+((-*)[A-Z\d])*)")
title_patt_regex = re.compile(r"([^\s]+\s)*")
bu_equiv_patt_regex = re.compile(r"[A-Z][\.A-Z]+\s[A-Z0-9]*")
cat_year_patt_regex = re.compile(r"(UG|GR)[0-9][0-9]")

inf = open('table.csv', 'w')
crs_writer = csv.writer(inf)
crs_writer.writerow(header)

for idx, line in enumerate(lines):

    if inst_patt_regex.search(line):
        inst = inst_patt_regex.search(line).group(0).strip()

    if '------------' in line:
        idx += 1
        line = lines[idx]
        while 'Bellarmine University' not in line:

            line_results = []
            line_results.append(inst)

            # split line into elements
            new_line, line_results = extract_elem(transf_crs_patt_regex, line, line_results)
            new_line, line_results = extract_elem(title_patt_regex, new_line, line_results)
            new_line, line_results = extract_elem(bu_equiv_patt_regex, new_line, line_results)
            new_line, line_results = extract_elem(cat_year_patt_regex, new_line, line_results)

            crs_writer.writerow(line_results)

            print line_results
            if idx + 1 < len(lines):
                idx += 1
                line = lines[idx]
            else:
                break

inf.close()
