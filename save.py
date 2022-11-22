import json
import os
import sys

import pymysql.cursors

if __name__ == '__main__':
    # Get logs
    if not (os.path.exists('logs.txt') and os.path.isfile('logs.txt')):
        exit()
    LOGS = json.load(open(f"logs.txt", "r"))

    # Connect to the database
    con = pymysql.connect(host=sys.argv[1],
                          user=sys.argv[2],
                          password=sys.argv[3],
                          database=sys.argv[4],
                          cursorclass=pymysql.cursors.DictCursor,
                          ssl={"fake_flag_to_enable_tls": True}
                          )
    try:
        with con.cursor() as cur:
            for email, info in LOGS.items():
                cur.execute("SELECT * FROM reward_logs WHERE email=%s", email)
                if record := cur.fetchone():
                    cur.execute(
                        "UPDATE reward_logs "
                        "SET last_check = %s, today_points = %s, total_points = %s "
                        "WHERE email=%s",
                        (
                            info['Last check'],
                            info.get("Today's points", 0),
                            info.get("Points", 0),
                            email
                        ))
                    con.commit()
                    print('update', email)
                else:
                    cur.execute(
                        "INSERT INTO reward_logs(email, last_check, today_points, total_points) "
                        "VALUES (%s, %s, %s, %s)",
                        (
                            email,
                            info['Last check'],
                            info.get("Today's points", 0),
                            info.get("Points", 0)
                        ))
                    con.commit()
                    print('insert', email)
    finally:
        con.close()
