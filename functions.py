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
          mycursor.execute(f"CREATE TABLE {tablename} ({con})")

def tester(mycursor, mydb, xtable, val):
    mycursor.execute(f"SELECT COUNT(*) FROM {xtable}")
    count = mycursor.fetchone()[0]
    if count == 0:
        placeholders = ", ".join(["%s"] * len(val[0]))
        mycursor.executemany(f"INSERT INTO {xtable} VALUES ({placeholders})", val)
        mydb.commit()

def testinsert(mycursor, mydb, envtables, mariadb):
  userval = [
              ("alex", "alex@live.no", "alexpassword", "karlgata 45", "kunde"),
              ("stian", "stian@live.no", "stianpassword", "karlgata 46", "kunde"),
              ("petter", "petter@live.no", "petterpassword", "karlgata 47", "kunde")
            ]
  productval = [
              ("Tine",  "gulost", 99.99, "Beste osten i byen", 1),
              ("Tine", "lett melk", 59.99, "Beste melken i byen", 1)
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
      tester(mycursor, mydb, utable, userval, envtables)
      tester(mycursor, mydb, ptable, productval, envtables)
  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")