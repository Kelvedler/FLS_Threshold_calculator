import sqlite3

if __name__ == "__main__":
    db_conn = sqlite3.connect("AC data")
    db_cursor = db_conn.cursor()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS acData (
        reg_num TEXT PRIMARY KEY,
        flight_h REAL,
        flight_c REAL,
        flight_h_daily REAL,
        flight_c_daily REAL,
        f_c_th_75x100 REAL,
        f_c_th_56x75 REAL
    )""")
    db_conn.commit()
    db_conn.close()
