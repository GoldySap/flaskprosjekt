import readchar

options = ["Add content", "View content", "Tests and defaults", "Exit"]
selected = 0
tablename = ""
tablecontent = ""
tablecont = []

def dbcheck(mycursor, db):
    mycursor.execute("SHOW DATABASES")
    temp = [x[0] for x in mycursor]
    print("Current databases:", temp, "\nDesired database:", db)
    if db not in temp:
      print("Database not found. \nCreating Database...")
      mycursor.execute(f"CREATE DATABASE {db} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
      temp.append(db)
    print(f"Database created: {db}")

def tablecheck(mycursor, envtables, envtablecontent):
    mycursor.execute("SHOW TABLES")
    temp = [x[0] for x in mycursor]
    print("Current tables:", temp, "\nDesired tables:", envtables)
    for i, tablename in enumerate(envtables):
      con = envtablecontent[i]
      if tablename not in temp:
          print(f"Table '{tablename}' not found. Creating table...")
          try:
              mycursor.execute(f"CREATE TABLE {tablename} {con}")
              print(f"Table '{tablename}' created successfully.")
          except Exception as e:
              print(f"Error creating table '{tablename}': {e}")
      else:
          print(f"Table '{tablename}' already exists.")
    print("All desired tables present.")

def testinsert(mycursor, mydb, envtables, mariadb):
  val = [
              ("acdc", "high way to hell"),
              ("the ink spots", "we'll meet again"),
              ("the ink spots", "if i didn't care"),
            ]
  print("Test values:", val)
  inp = input("Insert test values? y/n ").lower()
  if inp.lower() != "y":
      print("Cancelled.")
      return
  try:
      atable = None
      stable = None
      for t in envtables:
          if "artist" in t.lower():
              atable = t
          elif "song" in t.lower():
              stable = t
      if not atable or not stable:
          print("Error: Could not find 'artist' or 'song' table in envtables.")
          return
      mycursor.execute(f"SELECT COUNT(*) FROM {atable}")
      artist_count = mycursor.fetchone()[0]
      if artist_count == 0:
          print("Inserting test artists...")
          unique_artists = list({artist for artist, _ in val})
          artist_inserts = [(artist,) for artist in unique_artists]
          mycursor.executemany(f"INSERT INTO {atable} (artistname) VALUES (%s)", artist_inserts)
          mydb.commit()
          print(f"{mycursor.rowcount} artists inserted.")
      else:
          print("Artists already exist, skipping artist insert.")
      mycursor.execute(f"SELECT COUNT(*) FROM {stable}")
      song_count = mycursor.fetchone()[0]
      if song_count == 0:
          print("Inserting test songs...")
          mycursor.execute(f"SELECT id, artistname FROM {atable}")
          artist_map = {name.lower(): aid for aid, name in mycursor.fetchall()}
          sints = []
          for artistname, songname in val:
              aid = artist_map.get(artistname.lower())
              if aid:
                  sints.append((songname, aid))
              else:
                  print(f"Warning: Artist '{artistname}' not found, skipping song '{songname}'")
          if sints:
              mycursor.executemany(f"INSERT INTO {stable} (songname, artistid) VALUES (%s, %s)", sints)
              mydb.commit()
              print(f"{mycursor.rowcount} songs inserted.")
      else:
          print("Songs already exist, skipping song insert.")
      print("Test insert completed successfully.")
  except mariadb.Error as e:
      print(f"Error connecting to MariaDB: {e}")

def insert(mycursor, mydb):
    t = tselector(mycursor)
    print(f"\nSelected tabel: {t}")
    if t == "artist":
        count = int(input("How many artist to add: "))
        for _ in range(count):
          aname = input("Artistname: ").lower()
          mycursor.execute("SELECT id FROM artist WHERE artistname = %s", (aname,))
          res = mycursor.fetchone()
          if res:
              print(f"Artist: '{aname}' already exist.")
          else:
              mycursor.execute("INSERT INTO artist (artistname) VALUES (%s)", (aname,))
              mydb.commit()
              print(f"Artist '{aname}' added.")
    elif t == "song":
        count = int(input("How many song to add: "))
        for _ in range(count):
          sname = input("Songname: ").lower()
          aname = input("Artistname: ").lower()
          mycursor.execute("SELECT id FROM artist WHERE artistname = %s", (aname,))
          res = mycursor.fetchone()
          if res:
              aid = res[0]
          else:
              mycursor.execute("INSERT INTO artist (artistname) VALUES (%s)", (aname,))
              mydb.commit()
              aid = mycursor.lastrowid
              print(f"Artist '{aname}' added automatically.")
          mycursor.execute(
              "INSERT INTO song (songname, artistid) VALUES (%s, %s)",
              (sname, aid)
          )
          mydb.commit()
          print(f"Song: '{sname}', added with artist: '{aname}'.")

def tselector(mycursor):
    mycursor.execute("SHOW TABLES")
    temp = [x[0] for x in mycursor]
    vs = []
    while True:
        print("Avalible tables:", temp)
        for i, string in enumerate(temp):
          print(f"{string} - {i + 1}")
          vs.append((i + 1, string))
        key = readchar.readkey()
        if key.isdigit():
          key = int(key)
          for number, string in vs:
            if key == int(number):
              return string
            else:
              print(f"Invalid {key}. Try again:")

def spesifikk(mycursor, t):
  while True:
      print(
      "\nSearch Options:" \
      "\nView all content - 1" \
      "\nSearch category content - 2" \
      "\nSearch spesifikk content - 3"
        )
      key = readchar.readkey()
      if key.isdigit():
        key = int(key)
        match key:
          case 1:
              print(f"\nYou chose option: {key}\n")
              mycursor.execute(f"SELECT * FROM {t}")
              res = mycursor.fetchall()
              for x in res:
                print(x)
              break
          case 2:
              print(f"\nYou chose option: {key}\n")
              mycursor.execute(f"SELECT * FROM {t} LIMIT 0")
              dc = [cl[0] for cl in mycursor.description]
              if "id" in dc:
                dc.remove("id")
              print("Categories:", dc)
              c = input("Which category to search from: ")
              sql = f"SELECT {c} FROM {t};"
              mycursor.execute(sql)
              res = mycursor.fetchall()
              for x in res:
                print(x)
              break
          case 3:
              print(f"\nYou chose option: {key}\n")
              mycursor.execute(f"SELECT * FROM {t} LIMIT 0")
              dc = [cl[0] for cl in mycursor.description]
              if "id" in dc:
                dc.remove("id")
              print("Categories:", dc)
              c = input("Which category to search from: ")
              sql = f"SELECT {c} FROM {t};"
              mycursor.execute(sql)
              res = mycursor.fetchall()
              for x in res:
                print(x)
              o = input("What to search for in the category: ")
              if any(o.lower() == str(x[0]).lower() for x in res):
                sql = f"SELECT * FROM {t} WHERE {c} = %s"
                mycursor.execute(sql, (o,))
                res = mycursor.fetchall()
                for x in res:
                  print(f"{x}")
              else:
                print("Invalid search. Try again.")
          case _:
            print(f"\n{key} is not allowed. Try again.\n")
      else:
        print(f"\n{key} is not allowed. Try again.\n")

def alter(mycursor, mydb, t):
  while True:
    if t.lower() == "artist":
        c = "artistname"
        sql = f"SELECT {c} FROM {t};"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        for x in res:
          print(x)
        name = input("Artist name to modify: ").strip()
        mycursor.execute(f"SELECT id, {c} FROM {t} WHERE artistname = %s", (name,))
        artist = mycursor.fetchone()
        if not artist:
            print("Artist not found.")
        artist_id = artist[0]
        new_name = input("New artist name: ").strip()
        mycursor.execute("SELECT COUNT(*) FROM song WHERE artistid = %s", (artist_id,))
        linked_songs = mycursor.fetchone()[0]
        if linked_songs > 0:
            print(f"\nArtist '{name}' has {linked_songs} linked song(s)." \
                  "\nRename artist and delete songs. - 1" \
                  "\nRename artist, make a duplicate of the old artist and reassign songs. - 2" \
                  "\nCancel. - 3"
                  )
            key = readchar.readkey()
            if key.isdigit():
              key = int(key)
              match key:
                case 1:
                    mycursor.execute("DELETE FROM song WHERE artistid = %s", (artist_id,))
                    mycursor.execute("UPDATE artist SET artistname = %s WHERE id = %s", (new_name, artist_id))
                    mydb.commit()
                    print(f"Renamed artist '{name}' to '{new_name}'")
                    break
                case 2:
                    mycursor.execute("INSERT INTO artist (artistname) VALUES (%s)", (artist,))
                    mydb.commit()
                    aid = mycursor.lastrowid
                    mycursor.execute("UPDATE song SET artistid = %s WHERE artistid = %s", (aid, artist_id))
                    mydb.commit()
                    mycursor.execute("UPDATE artist SET artistname = %s WHERE id = %s", (new_name, artist_id))
                    mydb.commit()
                    print(f"Created new artist '{new_name}' and reassigned all songs.")
                    break
                case _:
                    print("Cancelled.")
                    break
        else:
            mycursor.execute("UPDATE artist SET artistname = %s WHERE id = %s", (new_name, artist_id))
            mydb.commit()
            print(f"Artist '{name}' renamed to '{new_name}'.")
            break
    elif t.lower() == "song":
        song = input("Song name to modify: ").strip()
        mycursor.execute("SELECT id, songname, artistid FROM song WHERE songname = %s", (song,))
        sdata = mycursor.fetchone()
        if not sdata:
            print("Song not found.")
            break
        song_id, old_name, artist_id = sdata
        print(f"Editing song: {old_name}")
        new_song_name = input("Enter new song name (or press Enter to keep current): ").strip()
        new_artist_name = input("Enter new artist name (or press Enter to keep current): ").strip()
        if new_song_name:
            mycursor.execute("UPDATE song SET songname = %s WHERE id = %s", (new_song_name, song_id))
            mydb.commit()
            print(f"Song renamed to '{new_song_name}'")
        if new_artist_name:
            mycursor.execute("SELECT id FROM artist WHERE artistname = %s", (new_artist_name,))
            artist = mycursor.fetchone()
            if not artist:
                print(f"Artist '{new_artist_name}' not found.")
                create = input("Create this artist? (y/n): ").strip().lower()
                if create == "y":
                    mycursor.execute("INSERT INTO artist (artistname) VALUES (%s)", (new_artist_name,))
                    mydb.commit()
                    new_artist_id = mycursor.lastrowid
                    print(f"Created new artist '{new_artist_name}'")
                    break
                else:
                    print("Artist change cancelled.")
                    break
            else:
                new_artist_id = artist[0]
            mycursor.execute("UPDATE song SET artistid = %s WHERE id = %s", (new_artist_id, song_id))
            mydb.commit()
            print(f"Updated artist for song '{new_song_name or old_name}' → '{new_artist_name}'")
            break

def deletionhandler(mycursor, mydb, db):
  while True:
    print(
            "\nDeletion Menu Options:" \
            "\nDelete specific data - 1" \
            "\nWipe all data (clear all tables) - 2" \
            "\nDelete database - 3" \
            "\nExit - 4"
        )
    key = readchar.readkey()
    if key.isdigit():
      key = int(key)
      match key:
        case 1:
          print(f"\nYou chose option: {key}\n")
          t = tselector(mycursor)
          print(f"\nSelected table: {t}")
          mycursor.execute(f"SELECT * FROM {t} LIMIT 0")
          dc = [cl[0] for cl in mycursor.description]
          if "id" in dc:
            dc.remove("id")
          print("Categories:", dc)
          c = input("Which category to search from: ")
          sql = f"SELECT {c} FROM {t};"
          mycursor.execute(sql)
          res = mycursor.fetchall()
          for x in res:
            print(x)
          v = input(f"Value for '{c}' to delete: ").strip()
          if t.lower() == "artist":
              mycursor.execute("SELECT id FROM artist WHERE artistname = %s OR id = %s", (v, v))
              artist_data = mycursor.fetchone()
              if not artist_data:
                  print("Artist not found.")
                  return
              aid = artist_data[0]
              mycursor.execute("SELECT COUNT(*) FROM song WHERE artistid = %s", (aid,))
              song_count = mycursor.fetchone()[0]
              if song_count > 0:
                  print(f"\nArtist has {song_count} linked song(s)." \
                        "\nDelete the artist AND all their songs - 1" \
                        "\nKeep the songs but set their artist to 'Unknown' - 2" \
                        "\nCancel - 3"
                        )
                  key = readchar.readkey()
                  if key.isdigit():
                    key = int(key)
                    match key:
                      case 1:
                        mycursor.execute("DELETE FROM song WHERE artistid = %s", (aid,))
                        mycursor.execute("DELETE FROM artist WHERE id = %s", (aid,))
                        mydb.commit()
                        print(f"Artist and linked songs deleted.")
                      case 2:
                        mycursor.execute("SELECT id FROM artist WHERE artistname = 'Unknown'")
                        unknown = mycursor.fetchone()
                        if not unknown:
                            mycursor.execute("INSERT INTO artist (artistname) VALUES ('Unknown')")
                            mydb.commit()
                            uid = mycursor.lastrowid
                            print("Created fallback artist: 'Unknown'")
                        else:
                            uid = unknown[0]
                        mycursor.execute("UPDATE song SET artistid = %s WHERE artistid = %s", (uid, aid))
                        mycursor.execute("DELETE FROM artist WHERE id = %s", (aid,))
                        mydb.commit()
                        print("Reassigned songs to 'Unknown' and deleted artist.")
                      case _:
                        print("Action cancelled.")
                        break
              else:
                  mycursor.execute("DELETE FROM artist WHERE id = %s OR artistname = %s", (v, v))
                  mydb.commit()
                  print(f"Artist '{v}' deleted successfully.")
          elif t.lower() == "song":
              mycursor.execute(f"SELECT id, songname FROM song WHERE {c} = %s", (v,))
              sd = mycursor.fetchone()
              if not sd:
                  print("Song not found.")
                  return
              confirm = input(f"Are you sure you want to delete song '{sd[1]}'? (y/n): ").lower()
              if confirm == "y":
                  mycursor.execute("DELETE FROM song WHERE id = %s", (sd[0],))
                  mydb.commit()
                  print(f"Deleted song '{sd[1]}'.")
              else:
                  print("Action cancelled.")
          else:
              confirm = input(f"Are you sure you want to delete from '{t}' where '{c}' = '{v}'? (y/n): ").lower()
              if confirm == "y":
                  sql = f"DELETE FROM {t} WHERE {c} = %s"
                  mycursor.execute(sql, (v,))
                  mydb.commit()
                  print("Entry deleted successfully.")
                  break
              else:
                  print("Action cancelled.")
        case 2:
          print(f"\nYou chose option: {key}\n")
          mycursor.execute("SHOW TABLES")
          tables = [x[0] for x in mycursor]
          confirm = input(f"Are you sure you want to DELETE ALL TABLE DATA PERMANENTLY? y/n: ").lower()
          if confirm == "y":
            for i, t in enumerate(reversed(tables)):
              print(f"Wiping data from {t}...")
              mycursor.execute(f"DELETE FROM {t}")
              mycursor.execute(f"ALTER TABLE {t} AUTO_INCREMENT = 1")
              mydb.commit()
              print(f"Data wiped from: '{t}'.")
            break
          else:
              print("Wipe cancelled.")
        case 3:
              print(f"\nYou chose option: {key}\n")
              inp = input("Delete database y/n: ").lower()
              if inp == "y":
                print("\nDeleting the databse will remove all data permanently, \nand will result in this file closing due to the database's disappearance.")
                inp = input("Type DELETE to continue: ")
                if inp == "DELETE":
                  print("\nDeleting database...")
                  mycursor.execute(f"DROP DATABASE {db}")
                  mydb.commit()
                  break
        case 4:
              print(f"\nYou chose option: {key}\n")
              print("Exiting deletion menu...")
              mydb.close()
              break
        case _:
          print(f"\n{key} is not allowed. Try again.\n")
    else:
        print(f"\n{key} is not allowed. Try again.\n")