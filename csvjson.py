
import json
import csv
from io import StringIO

#
# Convert CSV input to JSON for easier manipulation
#
def csvtojson(data, dialect=csv.excel(), field_names=None):

    rdr = csv.reader(data, dialect=dialect)

    if field_names is None:
        field_names = rdr.__next__()
        if field_names[0][0] == '#':
            field_names[0] = field_names[0][1:]

    result = []
    for rec in rdr:
        res = {}
        for name,value in zip(field_names, rec):
            res[name] = value
        result.append(res)

    return result

#
# Convert basic diction/JSON into a CSV record.  The values
# must all be simple values that can be represented in a
# CSV field.
#
def jsontocsv(data, output_file=None, dialect=csv.excel()):
    if type(data) != type([]):
        data = [data]

    if len(data) == 0:
        return None

    field_names = sorted(data[0].keys())
    result = [dialect.delimiter.join(field_names)]

    return_result = False
    if output_file is None:
        output_file = StringIO()
        return_result = True

    writer = csv.writer(output_file, dialect=dialect)
    writer.writerow(['#' + field_names[0]] + field_names[1:])
    for r in data:
        row = [r[key] for key in field_names]
        writer.writerow(row)

    if not return_result:
        return

    output_file.seek(0,0)

    return [x.rstrip() for x in output_file.readlines()]
        
    
