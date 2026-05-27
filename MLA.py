import bcrypt
import sqlite3
from time import sleep

# --------- CLEAR SCREEN ---------

def clear_screen():
    print("\033[H\033[J", end="")

# --------- DATA BASE STRUCTURE ---------

class DataBase:

    def __init__(self):
        self.connection = sqlite3.connect("Musics.db")
        self.cursor = self.connection.cursor()
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS musics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song TEXT,
        album TEXT,
        artist TEXT,
        rating INTEGER
    )""")

    def new_song(self, song, album, artist, rating):
        self.cursor.execute("INSERT INTO musics (song , album, artist, rating) VALUES (?,?,?,?)", (song, album, artist, rating))
        self.connection.commit()

    def read(self):
        self.cursor.execute("SELECT * FROM musics")
        return self.cursor.fetchall()

    def get_max_id(self):
        self.cursor.execute("SELECT MAX(id) FROM musics")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0

    def find_by_id(self, find_id):
        self.cursor.execute("SELECT * FROM musics WHERE id = ? ", (find_id,))
        return self.cursor.fetchone()

    def update_song(self, upd_song, id_to_update):
        self.cursor.execute("UPDATE musics SET song= ? WHERE id = ? ", (upd_song, id_to_update))
        self.connection.commit()

    def update_album(self, upd_album, id_to_update):
        self.cursor.execute("UPDATE musics SET album= ? WHERE id = ? ", (upd_album, id_to_update))
        self.connection.commit()

    def update_artist(self, upd_artist, id_to_update):
        self.cursor.execute("UPDATE musics SET artist= ? WHERE id = ? ", (upd_artist, id_to_update))
        self.connection.commit()

    def update_rating(self, upd_rating, id_to_update):
        self.cursor.execute("UPDATE musics SET rating= ? WHERE id = ? ", (upd_rating, id_to_update))
        self.connection.commit()

    def delete_song(self, id_to_delete):
        self.cursor.execute("DELETE FROM musics WHERE id = ? ", (id_to_delete,))
        self.connection.commit()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()
        print("Database connection closed.")

    def __del__(self):
        try:
            self.connection.close()
        except Exception:
            pass

# --------- USER DATA BASE STRUCTURE ---------

class UserDataBase:

    def __init__(self):
        self.connection = sqlite3.connect("Musics.db")
        self.cursor = self.connection.cursor()
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        type TEXT
    )""")

    def read(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_super_admin_id(self):
        self.cursor.execute("SELECT id FROM users WHERE type = 'Super Admin' LIMIT 1")
        row = self.cursor.fetchone()
        return int(row[0]) if row is not None else None

    def find_by_id(self, find_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ? ", (find_id,))
        return self.cursor.fetchone()

    def check_user_availability(self, login_username):
        self.cursor.execute("SELECT * FROM users WHERE username = ? ", (login_username,))
        return self.cursor.fetchone()

    def new_user(self, user, hashed_password, login_type):
        self.cursor.execute("INSERT INTO users (username, password, type) VALUES (?,?,?)", (user, hashed_password, login_type))
        self.connection.commit()

    def login_db(self, login_username, login_password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? ", (login_username,))
        user = self.cursor.fetchone()
        if not user:
            return None
        else:
            hashed_password = user[2]
            login_type = user[3]
            login_id = user[0]
            if bcrypt.checkpw(login_password.encode(), hashed_password.encode()):
                return login_id, login_type
            else:
                return None

    def close_connection(self):
        self.connection.commit()
        self.connection.close()
        print("User database connection closed.")

    def is_empty(self):
        self.cursor.execute("SELECT 1 FROM users LIMIT 1")
        return self.cursor.fetchone() is None

    def promote_demote(self, position, id_to_update):
        self.cursor.execute("UPDATE users SET type=? WHERE id=?", (position, id_to_update))
        self.connection.commit()

    def __del__(self):
        try:
            self.connection.close()
        except Exception:
            pass

# --------- MENU STRUCTURE ---------

class Menu:

    def __init__(self):
        self.db = DataBase()
        self.userdb = UserDataBase()
        self.login_type = None
        self.login_id = None
        self.login_options = {
            "1" : self.login,
            "2" : self.signup
        }
        self.menu_options = {
            "1" : self.list_songs,
            "2" : self.add_song,
            "3" : self.update_song,
            "4" : self.delete_song,
            "5" : self.log_out,
            "0" : self.exit_system
        }
        self.admin_options = {
            "1": self.list_songs,
            "2": self.add_song,
            "3": self.update_song,
            "4": self.delete_song,
            "5": self.update_user,
            "6": self.log_out,
            "0": self.exit_system
        }

    def menu_screen(self):
        while True:

            clear_screen()
            print("-=" * 16)
            print()
            print("[1] - List songs")
            print("[2] - Add song")
            print("[3] - Update song")
            print("[4] - Delete song")
            print("[5] - Log out")
            print("[0] - Exit")
            print()
            print("-=" * 16)

            while True:
                choice = input("> ").strip()

                if choice in self.menu_options:
                    self.menu_options[choice]()
                    break
                else:
                    print("Invalid option, try again!")

    def admin_screen(self):
        while True:

            clear_screen()
            print("-=" * 16)
            print()
            print("[1] - List songs")
            print("[2] - Add song")
            print("[3] - Update song")
            print("[4] - Delete song")
            print("[5] - Promote/Demote users")
            print("[6] - Log out")
            print("[0] - Exit")
            print()
            print("-=" * 16)

            while True:
                choice = input("> ").strip()

                if choice in self.admin_options:
                    self.admin_options[choice]()
                    break
                else:
                    print("Invalid option, try again!")

    def login_screen(self):
        while True:

            clear_screen()
            print("-=" * 16)
            print()
            print("Login or Sing up")
            print()
            print("[1] - Login")
            print("[2] - Sign up")
            print()
            print("-=" * 16)

            while True:
                choice = input("> ").strip()

                if choice in self.login_options:
                    self.login_options[choice]()
                    break
                else:
                    print("Invalid option, try again!")
                    continue

    def login(self):
        clear_screen()
        while True:
            print("-=" * 16)
            print()
            username = input("Username: ").strip()
            password = input("Password: ")
            login = self.userdb.login_db(username, password)
            if not login:
                print("Invalid username or password")
            else:
                self.login_id, self.login_type = login
                if self.login_type == "common":
                    self.menu_screen()
                else:
                    self.admin_screen()

    def signup_method(self,access):
        while True:
            username = input("Username: ").strip()
            check_username = self.userdb.check_user_availability(username)
            if check_username is not None:
                print("Username not available!")
                continue
            else:
                password = input("Password: ")
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                self.userdb.new_user(username, hashed.decode(), access)
                return

    def signup(self):
        clear_screen()
        print("-=" * 16)
        print()
        if self.userdb.is_empty():
            print("The first sign up created is the Super Admin")
            self.signup_method("Super Admin")
        else:
            self.signup_method("common")

    def list_songs(self):
        songs = self.db.read()
        if not songs:
            print("Empty list")
            input("Press Enter to continue...")
            return
        else:
            for song in songs:
                print(f"Song {song[1]} | Album {song[2]} | Artist {song[3]} | Rating {song[4]}")
            input("Press Enter to continue...")
            return

    def add_song(self):
        if self.login_type == "common":
            print("You don't have permission to do that")
            sleep(3)
            return
        else:
            clear_screen()
            print("-=" * 16)
            print()
            print("Add new song!!")
            song = input("Song: ").title().strip()
            album = input("Album: ").title().strip()
            artist = input("Artist: ").title().strip()
            while True:
                try:
                    rating = int(input("Rating: "))
                except ValueError:
                    print("Invalid number!! (0-10) ")
                    continue
                else:
                    if 0 <= rating <=10:
                        self.db.new_song(song, album, artist, rating)
                        print("Song Added!!")
                        return
                    else:
                        print("Invalid number!! (0-10) ")
                        continue

    def print_song(self, song):
        clear_screen()
        print("-=" * 16)
        print()
        print(f"Song {song[1]} | Album {song[2]} | Artist {song[3]} | Rating {song[4]}")
        print()

    def update_song(self):
        if self.login_type == "common":
            print("You don't have permission to do that")
            sleep(3)
            return
        else:
            clear_screen()
            max_id = self.db.get_max_id()
            if max_id == 0:
                print("Empty list")
            else:
                while True:
                    print("Which song do you wany to update? (ID) ")
                    try:
                        choice_id = int(input("> ").strip())
                    except ValueError:
                        print("Invalid ID")
                        continue
                    else:
                        if choice_id > max_id or choice_id <= 0:
                            print("Invalid ID")
                            continue
                        else:
                            song = self.db.find_by_id(choice_id)
                            if not song:
                                print("Invalid ID")
                                continue
                            else:
                                self.print_song(song)
                                print("What do you want to update?")
                                print("[1] - Song")
                                print("[2] - Album")
                                print("[3] - Artist")
                                print("[4] - Rating")
                                print("[5] - Another song")
                                print("[0] - Exit")

                                while True:
                                    choices = ["1","2","3","4","5","0"]
                                    choice = input("> ").strip()
                                    if choice in choices:
                                        break
                                    else:
                                        print("Invalid choice")
                                        continue

                                if choice == "1":
                                    self.print_song(song)
                                    print("New song:")
                                    upd_song = input("> ")
                                    self.db.update_song(upd_song, choice_id)
                                    print("Song updated!")
                                    sleep(3)
                                    return
                                elif choice == "2":
                                    self.print_song(song)
                                    print("New album:")
                                    upd_album = input("> ")
                                    self.db.update_album(upd_album, choice_id)
                                    print("Album updated!")
                                    sleep(3)
                                    return
                                elif choice == "3":
                                    self.print_song(song)
                                    print("New artist:")
                                    upd_artist = input("> ")
                                    self.db.update_artist(upd_artist, choice_id)
                                    print("Artist updated!")
                                    sleep(3)
                                    return
                                elif choice == "4":
                                    self.print_song(song)
                                    print("New Rating:")
                                    while True:
                                        try:
                                            upd_rating = int(input("> "))
                                        except ValueError:
                                            print("Invalid number!! (0-10)")
                                            continue
                                        else:
                                            if 0 <= upd_rating <= 10:
                                                self.db.update_rating(upd_rating, choice_id)
                                                print("Rating updated!")
                                                sleep(3)
                                                return
                                            else:
                                                print("Invalid number!! (0-10)")
                                                continue
                                elif choice == "5":
                                    continue
                                elif choice == "0":
                                    return

    def delete_song(self):
        if self.login_type == "common":
            print("You don't have permission to do that")
            sleep(3)
            return
        else:
            clear_screen()
            max_id = self.db.get_max_id()
            if max_id == 0:
                print("Empty list")
            else:
                while True:
                    print("Which song do you wany to delete? (ID) ")
                    try:
                        choice_id = int(input("> ").strip())
                    except ValueError:
                        print("Invalid ID")
                        continue
                    else:
                        if choice_id > max_id or choice_id <= 0:
                            print("Invalid ID")
                            continue
                        else:
                            song = self.db.find_by_id(choice_id)
                            if not song:
                                print("Invalid ID")
                                continue
                            else:
                                while True:
                                    self.print_song(song)
                                    print("Are you sure you want to delete this song? (Y/N)")
                                    choice = input("> ").upper().strip()
                                    if choice == "Y":
                                        self.db.delete_song(choice_id)
                                        print("Song deleted")
                                        sleep(3)
                                        return
                                    elif choice =="N":
                                        print("Action canceled")
                                        sleep(3)
                                        return
                                    else:
                                        print("Invalid answer, try again!")
                                        continue

    def update_user_method(self, action, user, position):
        while True:
            status = "demoted" if action == "demote" else "promoted"
            print(f"Are you sure you want to {action} {user[1]}? (Y/N)")
            choice = input("> ").strip().upper()
            if choice == "N":
                print("Canceling operation...")
                sleep(3)
                return
            elif choice == "Y":
                self.userdb.promote_demote(position, user[0])
                print(f"User: {user[1]} {status} successfully")
                sleep(3)
                return
            else:
                print("Invalid answer")
                continue

    def update_user(self):
        if self.login_type == "common":
            print("You don't have permission to do that")
            sleep(3)
            return
        users = self.userdb.read()
        for user in users:
            print(f"ID: {user[0]} | Username: {user[1]} | Position {user[3]}")
        super_id = self.userdb.get_super_admin_id()
        if super_id is None:
            raise RuntimeError("No Super Admin found")
        while True:
            choice = input("Which user do you want to promote or demote? (ID) (E to exit)\n> ").strip()
            if choice.upper() == "E":
                print("Returning...")
                sleep(3)
                return
            if not choice.isdigit():
                print("Please enter a numeric ID")
                continue
            choice_id = int(choice)
            if choice_id == int(self.login_id):
                print("You can't promote/demote yourself")
                continue
            if choice_id == int(super_id):
                print("You can't demote the Super Admin")
                continue
            user = self.userdb.find_by_id(choice_id)
            if user is None:
                print("No user with that ID")
                continue
            print(f"ID: {user[0]} | Username: {user[1]} | Position {user[3]}")
            if user[3] == "common":
                self.update_user_method("promote", user, "admin")
            else:
                if self.login_type == "admin":
                    print("Only the Super Admin has permission to demote.")
                    sleep(3)
                    continue
                self.update_user_method("demote", user, "common")

    def log_out(self):
        while True:
            clear_screen()
            print("Are you sure you want to Logout? (Y/N)")
            choice = input("> ").upper().strip()
            if choice == "Y":
                self.login_type = None
                self.login_id = None
                self.login_screen()
            elif choice == "N":
                print("Action canceled")
                sleep(3)
                return
            else:
                print("Invalid answer, try again!")
                continue
    def exit_system(self):
        print("Exiting and closing database...")
        self.db.close_connection()
        self.userdb.close_connection()
        exit()

if __name__ == "__main__":
    app = Menu()
    app.login_screen()