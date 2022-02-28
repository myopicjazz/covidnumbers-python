from datetime import datetime, timedelta
import requests
import csv


# scrapes data off of county github page
def get_new_data():
    # gets data table from the web and saves it as raw_data.txt file
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    r = requests.get(url, allow_redirects=True)
    open('raw_county_data.csv', 'wb').write(r.content)
    sort_data('raw_county_data.csv', 'new_county_file.csv')
    # gets data table from the web and saves it as raw_data.txt file
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    r = requests.get(url, allow_redirects=True)
    open('raw_state_data.csv', 'wb').write(r.content)
    sort_data('raw_state_data.csv', 'new_state_file.csv')


# sorts formatted text file by FIPS number
def sort_data(input_file, output_file):
    # opens raw_county_file.csv or raw_state_file.csv
    data = csv.reader(open(input_file), delimiter=',')
    # sorts output file by county or state column
    sortedlist = sorted(data, key=lambda row: row[1])
    # creates new_file.csv and writes sorted data to it row by row
    with open(output_file, 'w') as f:
        fileWriter = csv.writer(f, delimiter=',')
        for row in sortedlist:
            fileWriter.writerow(row)
    # closes f
    f.close


# get today's datetime, srips off milliseconds
current_datetime = datetime.today().replace(microsecond=0)
# declare and initialize get_csv variable
get_csv = 'no'
# create list for each row's data
county_entry = []
# list of states to check
states_list = ['Arkansas', 'Massachusetts', 'Wisconsin', 'Oklahoma']
# list of counties to check
county_fips_list = ['05007', '25025', '05143', '40021', '55063', '55023', '55123']
all_states = []
all_counties = []
# list of counties that match numbers in county_fips_list
local_counties = []
# list of all counties in states in states_list
state_counties = []
# create list for each row's data
state_entry = []
# list of top five states in nation
top_five_states = []
# list of counties with yesterday's date
recent_counties = []
# list of states with yesterday's date
recent_states = []
# list of top five counties from each state
top_five_counties = []

# open last_checked.txt file
f = open("last_checked.txt", 'r+')
# read first (only) row
first_row = f.readline()
# remove trailing newlines
first_row = first_row.rstrip('\r\n')
# convert first row to datetime
last_retrieved = datetime.strptime(first_row, '%Y-%m-%d %H:%M:%S')
# get difference between current datetime and last time the online
# data was checked
difference = current_datetime - last_retrieved
# if it has been at least six hours since the online data was
# last retrieved, do this
if difference >= timedelta(hours=6):
    # move back to very beginning of file
    f.seek(0, 0)
    # overwrite previous date in first row with today's date
    f.write(str(current_datetime))
    # flip get_csv to yes so script will get a new data set from online
    get_csv = 'yes'
# close file
f.close

# if the program has not yet been run today, the
# get_new_data, format_data, and sort_data functions are called
if get_csv == 'yes':
    get_new_data()

# open new_county_file.csv
with open('new_county_file.csv', 'r') as csvfileone:
    # create new csv.reader
    ff = csv.reader(csvfileone)

    # goes through new_county_file row by row
    for row in ff:
        # skips header row in csv file
        if row[0] != 'date':
            county_entry.append(row[0])
            county_entry.append(row[1])
            county_entry.append(row[2])
            county_entry.append(row[3])
            county_entry.append(row[4])
            county_entry.append(row[5])
            all_counties.append(county_entry)
        # clear county_entry list for next row of items
        county_entry = []
# closes csfile
csvfileone.close

# open new_state_file_csv
with open('new_state_file.csv', 'r') as csvfiletwo:
    # create new csv.reader
    ff = csv.reader(csvfiletwo)

    # go through new_state_file row by row
    for row in ff:
        # skips header row in csv file
        if row[0] != 'date':
            state_entry.append(row[0])
            state_entry.append(row[1])
            state_entry.append(row[2])
            state_entry.append(row[3])
            state_entry.append(row[4])
            all_states.append(state_entry)
        # clear state_entry list for next row of items
        state_entry = []
# closes csfile
csvfiletwo.close

# sort all_states list by date reported descending, then by number of
# infections descending
all_counties.sort(key=lambda x: (datetime.strptime(x[0], '%Y-%m-%d'), int(x[4])), reverse=True)

# sort all_states list by date reported descending, then by number of infections descending
all_states.sort(key=lambda x: (datetime.strptime(x[0], '%Y-%m-%d'), int(x[3])), reverse=True)

# gets most recent date from first entry in all_states after having been
# sorted by date descending
latest_date = datetime.strptime(all_states[0][0], '%Y-%m-%d')

# populates recent_states list with entries matching most recent date within
# last 10 days
for state in all_states:
    if datetime.strptime(state[0], '%Y-%m-%d') >= latest_date- timedelta(days=9):
        recent_states.append(state)

# top five states with most infections
top_five_states = recent_states[:5]

# create list of all county entries within last 10 days so long as there is
# a valid county name
for entry in all_counties:
    if datetime.strptime(entry[0], '%Y-%m-%d') >= latest_date - timedelta(days=9) and entry[3]:
        recent_counties.append(entry)

# populate state_counties list with states matching entries in state_list
for state in states_list:
    for county in recent_counties:
        # if state entries match
        if state == county[2]:
            state_counties.append(county)

# sort recent states by state name
recent_states.sort(key=lambda x: (x[1]))

# populates top_five_counties list with counties matching entries in state_list
for state in states_list:
    # c counter is reset to 0 after five county entries have been added to
    # top_five_counties list. they are already grouped by state name
    c = 0
    for county in recent_counties:
        # if state entries match and counter <= 4
        if state == county[2] and c <= 4:
            top_five_counties.append(county)
            c += 1

# uses state_counties to populate local_counties with counties listed in
# county_fips_list
for entry in state_counties:
    for fips in county_fips_list:
        if entry[3] == fips:
            local_counties.append(entry)

# sorts local_counties by county
local_counties.sort(key=lambda x: (x[1]))

# print header
print('')
print('************************ TOP STATES NATIONALLY *************************')
print('Date\t\tState\t\tInfections\tDeaths')

for entry in top_five_states:
    # prints entries in top_five_states list
    if len(entry[1]) <= 7:
        print(entry[0] + '\t' + entry[1] + '\t\t' + entry[3] + '\t\t' + entry[4])
    else:
        print(entry[0] + '\t' + entry[1] + '\t' + entry[3] + '\t\t' + entry[4])

# print header
print('')
print('************************ SELECTED STATES *******************************')
print('Date\t\tState\t\tInfections\tDeaths')

for entry in recent_states:
    # find and print records in recent_states list that match entries in the
    # state_list over last four days
    for state in states_list:
        if entry[1] == state and datetime.strptime(entry[0], '%Y-%m-%d') >= latest_date - timedelta(days=3):
            print(entry[0] + '\t' + entry[1] + '\t' + entry[3] + '\t\t' + entry[4])

# print header
print('')
print('************************ TOP FIVE COUNTIES SELECTED STATEs *************')
print('Date\t\tCounty\t\tState\t\tInfections\tDeaths')

# prints entries in top_five_counties list
for entry in top_five_counties:
    if len(entry[1]) <= 7:
        print(entry[0] + '\t' + entry[1] + '\t\t' + entry[2] + '\t' + entry[4] + '\t\t' + entry[5])
    else:
        print(entry[0] + '\t' + entry[1] + '\t' + entry[2] + '\t' + entry[4] + '\t\t' + entry[5])

# print header
print('')
print('************************ SPECIFIC COUNTIES *****************************')
print('Date\t\tCounty\t\tState\t\tInfections\tDeaths')

for entry in local_counties:
    # only prints records from the last three days by comparing entry[0] from
    # each record
    # with current date minus four days
    if datetime.strptime(entry[0], '%Y-%m-%d') >= latest_date - timedelta(days=3):
        # if listings are for Benton County, add an extra tab after county
        # name for justification
        if len(entry[1]) <= 7:
            print(entry[0] + '\t' + entry[1] + '\t\t' + entry[2] + '\t' + entry[4] + '\t\t' + entry[5])
        else:
            print(entry[0] + '\t' + entry[1] + '\t' + entry[2] + '\t' + entry[4] + '\t\t' + entry[5])
