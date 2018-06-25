import requests
from zipfile import ZipFile
import os
import csv
import shutil

# Returns CSV reader object from a given world bank API url

def collect(url, add_last=False):
    if not os.path.exists('temp'):
        os.makedirs('temp')

    print('Collecting from ' + url)

    print('Downloading CSV zip file...')
    r = requests.get(url)

    print('Saving ZIP file with length of ' + str(len(r.content)))
    with open('temp/worldbank.zip', 'wb') as output:
        output.write(r.content)

    print('Extracting ZIP file...')
    zipFile = ZipFile('temp/worldbank.zip')
    zipFile.extractall('temp/worldbank/')

    # Multiple CSV files, like metadata, are downloaded. Find the main file
    main_file = onlyfiles = [f for f in os.listdir(
        'temp/worldbank/') if f.startswith('API_')]
    if len(main_file) != 1:
        sys.exit(
            'Found {} files beginning with API_, expecting 1'.format(len(main_file)))
    main_file = 'temp/worldbank/' + main_file[0]

    with open(main_file, 'rt') as file:
        data = csv.reader(file)
        output = []
        ignore_cols = []

        IGNORED_COL_NAMES = ['Indicator Name', 'Indicator Code']

        for y, row in enumerate(data):
            # Skip to the first real row, first 3 is metadata
            # Figure out which columns to ignore
            if y == 4:
                line = []
                for x, item in enumerate(row):
                    if item in IGNORED_COL_NAMES:
                        ignore_cols.append(x)
                    # Ignore data before 1990
                    elif item.isdigit() and int(item) > 1950 and int(item) < 1990:
                        ignore_cols.append(x)
                    # Ignore empty columns
                    elif len(item) == 0:
                        ignore_cols.append(x)
                    else:
                        line.append(item)

                if add_last:
                    line.extend(("Last", "From"))
                output.append(line)

            if y > 4:
                line = []
                last_col = (None, None)
                for x, item in enumerate(row):
                    if x in ignore_cols:
                        continue

                    if item.replace('.','',1).isdigit():
                        # output doesn't have ignored columns; find how many has been ignored
                        # so we can access the heading (year of data) for this row/col
                        already_ignored = len([_x for _x in ignore_cols if _x < x])
                        last_col = (item, output[0][x - already_ignored])

                    line.append(item)

                if add_last:
                    line.extend(last_col)
                output.append(line)

    print('Extracted CSV! Cleaning up...')
    shutil.rmtree('temp/worldbank/')
    return output
