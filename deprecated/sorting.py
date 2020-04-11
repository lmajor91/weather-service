import json
import sqlite3
import csv

class statement(): # container class
    # sqlite statements
    # incremental keys from 1 to ...
    mk_country_table = '''CREATE TABLE IF NOT EXISTS countries (country_id INTEGER PRIMARY KEY, 
                                            country_name TEXT NOT NULL, 
                                            alpha_2 TEXT NOT NULL);'''

    mk_city_table = '''CREATE TABLE IF NOT EXISTS cities (
                                        table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        country_id INTEGER NOT NULL,
                                        city_id INTEGER,
                                        country_code TEXT NOT NULL,
                                        city_name TEXT NOT NULL,
                                        state TEXT,
                                        UNIQUE(country_id, city_name, country_code, state),
                                        FOREIGN KEY (country_id) 
                                            REFERENCES countries (country_id));'''

    ins_country_table = '''INSERT INTO countries VALUES (?, ?);'''
    ins_city_table = '''INSERT INTO cities (country_id, city_id, country_code, city_name, state) VALUES (?, ?, ?, ?, ?);'''

    fetch_country_table = '''SELECT * FROM countries ORDER BY country_id;'''
    fetch_city_table = '''SELECT * FROM cities ORDER BY country_id;'''

def make_country_table(verbose=False):
    # making a connection to the database
    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()
    cursor.execute(statement.mk_country_table)

    # opening the JSON file to extract data into and populate the DB
    with open("slim-2.json", "r") as file_in:
        data = json.load(file_in)
        count = 1
        for country in data:
            try:
                if verbose: print("Inserting %s into the table" % country["name"])
                cursor.execute(statement.ins_country_table, (count, country["name"]))
                count += 1
                if verbose: print("Success")
            except Exception as e:
                if verbose: print(e)
        file_in.close()
    conn.close()

def make_city_table(verbose=False):
    # making a connection to the database
    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()
    fkey_country_dict = {}

    # sample output
    # {u'country': u'IR', u'state': u'', u'id': 833, u'coord': {u'lat': 34.330502, u'lon': 47.159401}, u'name': u'\u1e28e\u015f\u0101r-e Sef\u012bd'}
    
    # first
    # going to fetch all the alpha-2 codes from the countries table and make them the new name of the new table which holds the countries' cities
    # mainly just to populate the key value pair list
    
    # second
    # going to use key value pairs to direct where the cities go respective to each table
    
    try: # first
        # making the table if it doesnt exist
        try:
            if verbose: print("Making cities table")
            cursor.execute(statement.mk_city_table)
            if verbose: print("Success")
        except Exception as e:
            if verbose: print(e)

        cursor.execute(statement.fetch_country_table)
        for row in cursor.fetchall(): # need the sqlite3 db just for the foreign keys
            table_name = row[2]
            foreign_key = row[0]
            fkey_country_dict[table_name] = foreign_key

    except Exception as e:
        if verbose: print(e)

    # going to iterate through the file with the cities then add them to the database
    with open("city.list.min.json", "r") as file_in: # second
        data = json.load(file_in)
        for city in data:
            try:
                if verbose: print("Inserting city: %s, %s" % (city["country"], city["name"]))
                if city["state"]:
                    cursor.execute(statement.ins_city_table, (fkey_country_dict[city["country"]], city["id"], city["country"], city["name"], city["state"]))
                else:
                    cursor.execute(statement.ins_city_table, (fkey_country_dict[city["country"]], city["id"], city["country"], city["name"], None))
                if verbose: print("Success")
            except Exception as e:
                if verbose: print(e)

        conn.commit()
        file_in.close()

    conn.close()

    # returns 0 if there are no errors not dealt with
    return 0

def iter_through_temp(verbose=False):
    canada = []
    with open ("cities_in_canada", "r") as file_in:
        for line in file_in:
            t = line.split(": ")[1].strip("\n").split(", ")
            t[0] = t[0].decode("utf-8")
            t[1] = t[1].decode("utf-8")
            canada.append(t)
        file_in.close()

    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()

    # updating the database
    for city, province in canada:
        try: # trying to update the rows which have the city but not the province
            if verbose: print("Updating %s's province to %s" % (city, province))
            cursor.execute('UPDATE cities SET state = ? WHERE city_name IS ? AND country_code IS "CA" AND state IS NULL;', (province, city))
            if verbose: print("Success")
        except Exception as e: # if there is a failure that means that there are two of the same city, just different city IDs
            if "UNIQUE constraint failed" in str(e):
                try:
                    # asking sqlite3 for all the rows which have the specified city name and dont have any provinces attached to the row
                    cursor.execute("SELECT * FROM cities WHERE city_name IS ? AND country_code IS 'CA' AND state IS NULL AND city_id IS NOT NULL;", (city,))
                    row = cursor.fetchone()
                    if row: # if sqlite3 returned a row do something
                        if verbose: print("Updating city %s with ID %d with province %s" % (city, row[2], province))
                        cursor.execute('UPDATE cities SET state = ? WHERE city_id IS ? AND country_code IS "CA" AND state IS NULL;', (province, row[2],))
                        if verbose: print("Success")
                except Exception as e:
                    if verbose: print(e)
            else:
                pass
    
    conn.commit()
    conn.close()

def iter_through_csv(verbose=False):
    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()

    with open("cgn_canada_csv_eng.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            # split(',') [1] is the name of the city [11] is the name of the province / territory
            city, province = row[1].decode("utf-8"), row[11]

            try:
                if verbose: print("Updating city '%s' with province '%s'" % (city, province))
                cursor.execute('UPDATE cities SET state = ? WHERE city_name IS ? AND country_code IS "CA" AND state IS NULL;', (province, city,))
                if verbose: print("Success")
            except Exception as e:
                if verbose: print(e)
            else:
                pass

    conn.commit()
    conn.close()
    csvfile.close()

def correct_usa_states(verbose=False):
    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()

    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            state, abbrev, code = row
            del abbrev
            try:
                if verbose: print("Updating %s to %s" % (code, state))
                cursor.execute('UPDATE cities SET state = ? WHERE state IS ?', (state, code))
                if verbose: print("Success")
            except Exception as e:
                if verbose: print(e)

    conn.commit()
    conn.close()
    csvfile.close()

def make_id(verbose=False):
    # making a connection to the database
    conn = sqlite3.connect("../db/master.db")
    cursor = conn.cursor()

    try:
        # getting all the data
        cursor.execute("SELECT * FROM cities WHERE state IS NOT NULL;")
        # (table_id, country_id, city_id, country_code, city_name, state, state_id)
        city_rows = cursor.fetchall()

        cursor.execute("SELECT * FROM states;")
        # (state_id, state, cities, country_id)
        state_rows = cursor.fetchall()

        # joining the lists
        result = []
        for city in city_rows:
            city_id, cstate = city[2], city[5]
            for state in state_rows:
                state_id, sstate = state[0], state[1]
                if cstate == sstate:
                    result.append([city_id, state_id])
                else:
                    pass
        
        # updating the sqlite3 database
        for update in result:
            try:
                if verbose: print("Updating %s to its proper state %s" % (update[0], update[1]))
                cursor.execute("UPDATE city SET state_id = ? WHERE city_id IS ?;", (update[1], update[0]))
            except Exception as e:
                if verbose:
                    print(e)
            else:
                if verbose: print("Success")


    except Exception as e:
        if verbose: print(e)
    
    conn.commit()
    conn.close() 

def main():
    #make_city_table(verbose=True)
    #iter_through_temp(verbose=True)
    #iter_through_csv(verbose=True)
    #correct_usa_states(verbose=True)
    make_id(verbose=True)

    return 0

if __name__ == "__main__":
    main()