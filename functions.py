def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES;")
    temp = [x[0] for x in mycursor]
    if db not in temp:
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)

def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES;")
    temp = [x[0] for x in mycursor]
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} {con}")

def tester(mycursor, mydb, xtable, val):
    mycursor.execute(f"SELECT COUNT(*) FROM {xtable}")
    count = mycursor.fetchone()[0]
    if count == 0:
        mycursor.execute(f"SELECT * FROM {xtable} LIMIT 0")
        dc = [cl[0] for cl in mycursor.description]
        if "id" in dc:
          dc.remove("id")
        elif "time" in dc:
          dc.remove("time")
        colnames = ", ".join(f"`{c}`" for c in dc)
        print(colnames)
        placeholders = ", ".join(["%s"] * len(dc))
        mycursor.executemany(f"INSERT INTO {xtable} ({colnames}) VALUES ({placeholders})", val)
        mydb.commit()

def testinsert(mycursor, mydb, envtables, mariadb):
  userval = [
              ("alex", "alex@live.no", "alexpassword", "karlgata 45", "kunde"),
              ("stian", "stian@live.no", "stianpassword", "karlgata 46", "kunde"),
              ("petter", "petter@live.no", "petterpassword", "karlgata 47", "kunde")
            ]
  productval = [
              ("Tine",  "gulost", 99.9, "FOOD", "Beste osten i byen", 1),
              ("Tine", "lett melk", 59.9, "FOOD", "Beste melken i byen", 2)
            ]
  try:
      utable = None
      ptable = None
      for t in envtables:
          if "users" in t.lower():
              utable = t
          elif "products" in t.lower():
              ptable = t
      if not utable or not ptable:
          return
      tester(mycursor, mydb, utable, userval)
      tester(mycursor, mydb, ptable, productval)
  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")