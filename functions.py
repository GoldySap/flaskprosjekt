def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES")
    temp = [x[0] for x in mycursor]
    if db not in temp:
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)

def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES")
    temp = [x[0] for x in mycursor]
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          try:
              mycursor.execute(f"CREATE TABLE {tablename} {con}")
          except Exception as e:
              print(f"Error creating table '{tablename}': {e}")

def testinsert(mycursor, mydb, envtables, mariadb):
  userval = [
              ("alex", "alex@live.no", "", "karlgata 45", "kunde"),
              ("stian", "stian@live.no", "", "karlgata 46", "kunde"),
              ("petter", "petter@live.no", "", "karlgata 47", "kunde"),
            ]
  productval = [
              ("Tine gulost", 99.99, "Beste osten i byen", 1),
            ]
  try:
      atable = None
      stable = None
      for t in envtables:
          if "users" in t.lower():
              ptable = t
          if "products" in t.lower():
              atable = t
      if not ptable or not stable:
          return
      mycursor.execute(f"SELECT COUNT(*) FROM {atable}")
      user_count = mycursor.fetchone()[0]
      if user_count == 0:
          unique_users = list({user for user, _ in userval})
          user_inserts = [(user,) for user in unique_users]
          mycursor.execute(f"SELECT * FROM {t} LIMIT 0")
          dc = [cl[0] for cl in mycursor.description]
          mycursor.executemany(f"INSERT INTO {atable} ({dc[0]}) VALUES (%s)", user_inserts)
          mydb.commit()
      mycursor.execute(f"SELECT COUNT(*) FROM {stable}")
      product_count = mycursor.fetchone()[0]
      if product_count == 0:
          unique_products = list({product for product, _ in productval})
          product_inserts = [(product,) for product in unique_products]
          mycursor.execute(f"SELECT * FROM {t} LIMIT 0")
          dc = [cl[0] for cl in mycursor.description]
          mycursor.executemany(f"INSERT INTO {atable} ({dc[0]}) VALUES (%s)", product_inserts)
          mydb.commit()
  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")