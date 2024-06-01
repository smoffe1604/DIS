from flask import Flask, render_template, redirect, url_for, session, abort, request, flash, jsonify
import psycopg2
import threading

#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
import os
import glob
import pandas as pd
import random
import os 
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# set your own database name, username and password
db = "dbname='ryges_svampefinder' user='brianshaw' host='localhost' password=''"
DATABASE_URI = "dbname='ryges_svampefinder' user='brianshaw' host='localhost' password=''"
conn = psycopg2.connect(db)
cur = conn.cursor()

table_exist = False
#################################################################################
############################### Functions #######################################
#################################################################################
def create_table_sql():
    columns_sql = "id serial PRIMARY KEY, "
    numeric_types = ['cap-diameter', 'stem-height', 'stem-width']  
    with open("src/static/mushrooms.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader) 

        for header in headers:
            data_type = "varchar" 
            if header in numeric_types:
                data_type = "numeric" 
            columns_sql += f"{header.replace('-', '_')} {data_type}, "
    
    columns_sql = columns_sql.rstrip(', ') 
    final_sql = "CREATE TABLE IF NOT EXISTS mushrooms (" + columns_sql + ");"
    cur.execute(final_sql)
    conn.commit() 
    
def insert_data_from_csv():
    with open("src/static/mushrooms.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader) 

        headers = [h.replace('-', '_') for h in headers]  
        placeholders = ', '.join(['%s'] * len(headers)) 

        sql = f"INSERT INTO mushrooms ({', '.join(headers)}) VALUES ({placeholders})"

        for row in reader:
            row = [None if x == '' else float(x) if x.replace('.', '', 1).isdigit() else x for x in row]
            cur.execute(sql, row)

    conn.commit()
    print("All data inserted successfully.")

def database_operations():
    try:
        with psycopg2.connect(DATABASE_URI) as conn:
            with conn.cursor() as cur:
                create_table_sql()
                insert_data_from_csv()
                flash("Table created success")
    except psycopg2.Error as e:
        flash( f"An error occurred: {e}")

def drop_existing_tables(conn, cur):
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        for table in tables:
            print(f"Dropping table {table[0]}")
            cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
        conn.commit()

#################################################################################
################################# Routes ########################################
#################################################################################
@app.route('/')
def index():
    global table_exist
    try:
        with psycopg2.connect(DATABASE_URI) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('mushrooms',))
                table_exist = cur.fetchone()[0]
    except psycopg2.Error as e:
        print("Unable to connect to the database or query error")

    return render_template('index.html', table_exist = table_exist)

@app.route('/delete_table', methods = ['POST'])
def delete_table():
    try:
        with psycopg2.connect(DATABASE_URI) as conn:
            with conn.cursor() as cur:
                drop_existing_tables(conn, cur)
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()

    return redirect(url_for('index'))


@app.route('/process_table', methods=['POST'])
def process_table():
    return render_template('processingTable.html')


@app.route('/create_table', methods=['POST'])
def create_table():
    database_operations()
    return jsonify({"message": "Processing started"}), 202

@app.route('/success')
def success():
    return redirect(url_for('index'))

import re



@app.route('/submit_text', methods=['POST'])
def submit_text():
    cap_d = float(request.form['cap_d'])
    cap_shape = request.form['cap_shape']
    cap_surf = request.form['cap_surf']
    cap_color = request.form['cap_color']
    stem_h = float(request.form['stem_h'])
    stem_w = float(request.form['stem_w'])


    
    shape_patterns = {
        r"[bB][eE][lL][lL]": 'b',
        r"[cC][oO][nN][iI][cC][aA][lL]": 'c',
        r"[cC][oO][nN][vV][eE][xX]": 'x',
        r"[fF][lL][aA][tT]": 'f',
        r"[sS][uU][nN][kK][eE][nN]": 's',
        r"[sS][pP][hH][eE][rR][iI][cC][aA][lL]": 'p',
        r"[oO][tT][hH][eE][rR][sS]": 'o'
    }

    surface_patterns = {
        r"[fF][iI][bB][rR][oO][uU][sS]": 'i',
        r"[gG][rR][oO][oO][vV][eE][sS]": 'g',
        r"[sS][cC][aA][lL][yY]": 'y',
        r"[sS][mM][oO][oO][tT][hH]": 's',
        r"[sS][hH][iI][nN][yY]": 'h',
        r"[lL][eE][aA][tT][hH][eE][rR][yY]": 'l',
        r"[sS][iI][lL][kK][yY]": 'k',
        r"[sS][tT][iI][cC][kK][yY]": 't',
        r"[wW][rR][iI][nN][kK][lL][eE][dD]": 'w',
        r"[fF][lL][eE][sS][hH][yY]": 'e'
    }

    color_patterns = {
        r"[bB][rR][oO][wW][nN]": 'n',
        r"[bB][uU][fF][fF]": 'b',
        r"[gG][rR][aA][yY]": 'g',
        r"[gG][rR][eE][eE][nN]": 'r',
        r"[pP][iI][nN][kK]": 'p',
        r"[pP][uU][rR][pP][lL][eE]": 'u',
        r"[rR][eE][dD]": 'e',
        r"[wW][hH][iI][tT][eE]": 'w',
        r"[yY][eE][lL][lL][oO][wW]": 'y',
        r"[bB][lL][uU][eE]": 'l',
        r"[oO][rR][aA][nN][gG][eE]": 'o',
        r"[bB][lL][aA][cC][kK]": 'k'
    }

    def determine_cap_shape(input, patterns):
        for pattern, result in patterns.items():
            if re.search(pattern, input):
                return result
        return 'o'
    
    cap_shape = determine_cap_shape(cap_shape, shape_patterns)
    cap_surf = determine_cap_shape(cap_surf, surface_patterns)
    cap_color = determine_cap_shape(cap_color, color_patterns)


    cap_d_interval = 0.5
    stem_h_interval = 0.5
    stem_w_interval = 0.5

    rows = []
    column_names = []

    try:
        with psycopg2.connect(DATABASE_URI) as conn:
            with conn.cursor() as cur:
                condition1 = f"cap_diameter > {cap_d - cap_d_interval} AND cap_diameter < {cap_d + cap_d_interval}"
                condition2 = f"cap_shape = '{cap_shape}'"
                condition3 = f"cap_surface = '{cap_surf}'"
                condition4 = f"cap_color = '{cap_color}'"
                condition5 = f"stem_height > {stem_h - stem_h_interval} AND stem_height < {stem_h + stem_h_interval}"
                condition6 = f"stem_width > {stem_w - stem_w_interval} AND stem_width < {stem_w + stem_w_interval}"
                sql = f"SELECT * FROM mushrooms WHERE {condition1} AND {condition2} AND {condition3} AND {condition4} AND {condition5} AND {condition6}"
                cur.execute(sql + " LIMIT 0;")
                column_names = [desc[0] for desc in cur.description]
                
                cur.execute(sql + ";")
                print(rows)
                rows = cur.fetchall()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

    return render_template('show_table.html', columns=column_names, rows=rows)

@app.route('/show_table')
def show_table():
    rows = []
    column_names = []

    try:
        with psycopg2.connect(DATABASE_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM mushrooms LIMIT 0;")
                column_names = [desc[0] for desc in cur.description]
                cur.execute("SELECT * FROM mushrooms;")
                rows = cur.fetchall()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

    return render_template('show_table.html', columns=column_names, rows=rows[:200])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)