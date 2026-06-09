#app.py
from datetime import datetime, timedelta
import shutil
from werkzeug.utils import secure_filename
import re
from my_lib import Database_Manager
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from secure_password import encrypt_password, pwd_config
from flask import send_from_directory
import os
app = Flask(__name__)
app.secret_key = 'secret123'

def initialize_database():
    db = Database_Manager('flightsim_db.sql')
    # Users Table
    users_table_query = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id            INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name         TEXT NOT NULL,
        last_name          TEXT NOT NULL,
        preferred_username TEXT NOT NULL UNIQUE,
        email              TEXT NOT NULL UNIQUE,
        password_hash      TEXT NOT NULL,
        role               TEXT NOT NULL,
        msfs_version       TEXT
    );
    """
    db.run_save(users_table_query, values=())
    # Addons Table
    addons_table_query = """
    CREATE TABLE IF NOT EXISTS Addons (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        addon_id         TEXT NOT NULL UNIQUE,
        title            TEXT NOT NULL UNIQUE,
        description      TEXT,
        model_filename   TEXT,
        image_filename   TEXT,
        category         TEXT,
        version          TEXT,
        min_msfs_version TEXT,
        dependency       TEXT,
        developer        TEXT,
        uploader_id      INTEGER,
        download_count   INTEGER DEFAULT 0
    );
    """
    db.run_save(addons_table_query, values=())

    # Aircrafts Table
    aircrafts_table_query = """
    CREATE TABLE IF NOT EXISTS Aircrafts (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL UNIQUE,
        image_filename TEXT,
        max_speed     INTEGER,
        mtow          INTEGER,
        fuel_capacity INTEGER,
        range         INTEGER,
        climb_rate    INTEGER
    );
    """
    db.run_save(aircrafts_table_query, values=())

    aircraft_data = [
        ('Beechcraft Bonanza G36', 'bonanza_g36.jpg', 176, 3650, 444, 920, 1280),
        ('DA62', 'da62.jpg', 201, 2300, 326, 1270, 1280),
        ('Beechcraft King Air 350i', 'kingair_350i.jpg', 312, 6800, 1950, 1800, 2700),
        ('Pilatus PC-12', 'pc12.jpg', 285, 4740, 1210, 1560, 1920),
        ('TBM 930', 'tbm930.jpg', 330, 3350, 1100, 1730, 2400),
        ('Cirrus SR22', 'sr22.jpg', 213, 3600, 348, 1200, 1270),
        ('Cessna Citation CJ4', 'citation_cj4.jpg', 451, 7640, 3900, 2165, 3500),
        ('Airbus A320neo', 'a320neo.jpg', 470, 79000, 23857, 3500, 2400),
        ('Boeing 737-800', 'b737_800.jpg', 470, 79015, 26020, 2935, 2700),
        ('Spitfire Mk IX', 'spitfire_mkix.jpg', 408, 4050, 400, 450, 4700)
    ]

    insert_aircraft_query = """
    INSERT OR IGNORE INTO Aircrafts (name, image_filename, max_speed, mtow, fuel_capacity, range, climb_rate)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    for aircraft in aircraft_data:
        db.run_save(insert_aircraft_query, values=aircraft)
    db.close()

initialize_database()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    register_error = None

    if request.method == 'POST':
        form_type = request.form.get('form_type', 'login')
        # login page
        if form_type == 'login':
            username_or_email = request.form['username_or_email']
            password = request.form['password']

            db = Database_Manager('flightsim_db.sql')
            query = """
                SELECT user_id, preferred_username, password_hash, role 
                FROM Users 
                WHERE preferred_username=? OR email=?
            """
            result = db.search_all(query, values=(username_or_email, username_or_email))
            db.close()

            if result:
                user_id, uname, hash_pw, role = result[0]
                if pwd_config.verify(password, hash_pw):
                    session['user_id'] = user_id
                    session['username'] = uname
                    session['role'] = role
                    if role == "user":
                        return redirect('/user_main')
                    elif role == "admin":
                        return redirect('/admin_main')
                    elif role == "developer":
                        return redirect('/developer_main')

            error = "Invalid username/email or password."

        # register page
        elif form_type == 'register':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            preferred_username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form['role']
            privacy_code = request.form.get('privacy_code','')
            msfs_version = request.form.get('msfs_version', None)

            if password != confirm_password:
                register_error = "Passwords do not match."
            elif role == 'admin' and privacy_code != 'anar':
                register_error = "Invalid admin privacy code."
            else:
                db = Database_Manager('flightsim_db.sql')
                check_query = "SELECT * FROM Users WHERE preferred_username=? OR email=?"
                existing = db.search_all(check_query, values=(preferred_username, email))

                if existing:
                    register_error = "Username or email already exists."
                else:
                    password_hash = encrypt_password(password)
                    insert_query = """
                        INSERT INTO Users (first_name, last_name, preferred_username, email, password_hash, role, msfs_version)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    db.run_save(insert_query, values=(
                        first_name, last_name, preferred_username, email, password_hash, role, msfs_version
                    ))

                    user_id_query = "SELECT user_id FROM Users WHERE email=?"
                    new_user = db.search_one(user_id_query, (email,))

                    if new_user:
                        new_user_id = new_user[0]
                        create_library_for_role(new_user_id, role)
                    db.close()
                    return redirect('/login')
                db.close()
    return render_template('login.html', error=error, register_error=register_error)

def create_library_for_role(user_id, role):
    db = Database_Manager('flightsim_db.sql')

    # user case
    if role == 'user':
        table_name = f"user_library_{user_id}"
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                category TEXT,
                version TEXT,
                min_msfs_version TEXT,
                date_added TEXT,
                date_installed TEXT,
                status TEXT
            )
        """
        db.run_save(create_table_query, values=())

    # developer case
    elif role == 'developer':
        table_name = f"developer_library_{user_id}"
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                model_filename TEXT,
                image_filename TEXT,
                category TEXT,
                version TEXT,
                min_msfs_version TEXT,
                dependent_on TEXT,
                required_for TEXT,
                proposed_date TEXT,
                approved_date TEXT,
                status TEXT 
            )
        """
        db.run_save(create_table_query, values=())


    db.close()

@app.route('/user_main')
def user_main():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    #Getting the username from the session
    username = session.get('username', 'Guest')  # Default to 'Guest'

    db = Database_Manager('flightsim_db.sql')
    query = "SELECT * FROM Addons"
    addons = db.search_all(query, values=())
    db.close()
    #Passing the username to the template
    return render_template('user_main.html', addons=addons, username=username)

@app.route('/mylib_<int:user_id>')
def mylib(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect('/login')

    username = session.get('username', 'Guest')
    db = Database_Manager('flightsim_db.sql')
    user_msfs_record = db.search_one("SELECT msfs_version FROM Users WHERE user_id = ?", (user_id,))
    user_msfs_version = user_msfs_record[0] if user_msfs_record else "0.0"
    table_name = f"user_library_{user_id}"
    all_addons = db.search_all(f"SELECT * FROM {table_name}", values=())
    db.close()
    in_queue_addons = []
    installed_addons = []
    for addon in all_addons:
        if addon[7] == 'in_queue':
            in_queue_addons.append(addon)
        elif addon[7] == 'installed':
            installed_addons.append(addon)

    return render_template('mylib.html',
                           in_queue=in_queue_addons,
                           installed=installed_addons,
                           username=username,
                           user_msfs_version=user_msfs_version)

def get_user_msfs_version(db, user_id):
    user_data = db.search_one("SELECT msfs_version FROM Users WHERE user_id = ?", (user_id,))
    return user_data[0] if user_data else "0.0"

def get_user_library_titles(db, user_id, status=None):
    table_name = f"user_library_{user_id}"
    query = f"SELECT title FROM {table_name}"
    values = ()
    if status: query += " WHERE status = ?"; values = (status,)
    library_tuples = db.search_all(query, values=values)
    return {item[0] for item in library_tuples}

@app.route('/simple_add_to_library', methods=['POST'])
def simple_add_to_library():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    addon_id_str = data.get('addon_id')
    user_id = session['user_id']
    table_name = f"user_library_{user_id}"
    db = Database_Manager('flightsim_db.sql')

    query = "SELECT title, category, version, min_msfs_version FROM Addons WHERE addon_id = ?"
    addon_data = db.search_one(query, (addon_id_str,))
    if not addon_data:
        db.close()
        return jsonify({"status": "error", "message": "Addon not found."})

    title, category, version, min_msfs_version = addon_data

    exists = db.search_one(f"SELECT id FROM {table_name} WHERE title = ?", (title,))
    if exists:
        db.close()
        return jsonify({"status": "exists", "message": f"'{title}' is already in your library."})

    db.run_save(f"""
        INSERT INTO {table_name} (title, category, version, min_msfs_version, date_added, date_installed, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, category, version, min_msfs_version, (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), None, 'in_queue'))

    db.close()
    return jsonify({"status": "success", "message": f"'{title}' added to your library."})

@app.route('/install_step', methods=['POST'])
def install_step():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    step = data.get('step')
    user_library_id = data.get('user_library_id')
    user_id = session['user_id']

    db = Database_Manager('flightsim_db.sql')

    current_addon_record = db.search_one(f"SELECT * FROM user_library_{user_id} WHERE id = ?", (user_library_id,))
    if not current_addon_record: db.close(); return jsonify({"error": "Addon not found in your library."})

    current_addon_title = current_addon_record[1]
    current_addon_main = db.search_one("SELECT * FROM Addons WHERE title = ?", (current_addon_title,))
    if not current_addon_main: db.close(); return jsonify({"error": "Addon not found in main database."})

    # Case 1: Version Check
    if step == 'version_check':
        user_msfs = get_user_msfs_version(db, user_id)
        min_msfs = current_addon_main[8]
        if float(user_msfs) >= float(min_msfs):
            return jsonify({"next_step": "dependency_check", "dialog": {"title": "Version Check Passed",
                                                                        "text": f"MSFS Version {user_msfs} is compatible. Proceed to dependency check?",
                                                                        "buttons": ["Proceed", "Cancel"]}})
        else:
            return jsonify({"next_step": "dependency_check", "dialog": {"title": "Version Mismatch",
                                                                        "text": f"This addon requires MSFS {min_msfs}, but your version is {user_msfs}. Check dependencies anyway?",
                                                                        "buttons": ["Proceed Anyway", "Cancel"]}})

    # Case 2: Dependency check
    if step == 'dependency_check':
        # 1.Load data into memory once for stability and speed
        all_addons_raw = db.search_all("SELECT * FROM Addons", values=())
        addons_by_title = {addon[2]: addon for addon in all_addons_raw}
        addons_by_addon_id = {addon[1]: addon for addon in all_addons_raw}

        # 2.The recursive function now returns the chain it builds
        def find_deps_recursive(addon_title, path):
            # If we find a cycle, we stop recursing down this branch, but we don't signal an error. We return an empty list for this path.
            if addon_title in path:
                return []  #Stop traversal
            path.append(addon_title)

            addon = addons_by_title.get(addon_title)

            # Base case:addon has no dependency
            if not addon or not addon[9]:
                path.pop()
                return []  #Return an empty list for this path

            dep_id = addon[9].split(':', 1)[0]
            dep_addon = addons_by_addon_id.get(dep_id)

            if dep_addon:
                #Recurse and get the chain from the dependency
                deeper_chain = find_deps_recursive(dep_addon[2], list(path))
                #We append the current dependency to the chain returned by the deeper call
                path.pop()
                return deeper_chain + [dep_addon]

            path.pop()
            return []  #Return empty list if dependency not found

        # 3.Start the process.This will return the valid chain, even if a cycle was hit
        dependency_chain = find_deps_recursive(current_addon_title, [])

        # 4.Process the results
        if not dependency_chain:
            return jsonify({
                "next_step": "library_check",
                "addons_to_check": [current_addon_main],
                "dialog": {"title": "No Dependencies", "text": f"No dependencies found for {current_addon_title}.",
                           "buttons": ["Install", "Cancel"]}
            })

        # The full chain for the user includes the dependencies and the original addon.
        full_chain_to_check = dependency_chain + [current_addon_main]

        return jsonify({
            "next_step": "user_confirm_dependency_versions",
            "dependency_chain": full_chain_to_check
        })

    #Case 3: Library Check
    if step == 'library_check':
        addons_to_check = data.get('addons_to_check', [])
        #Add the original addon to the list to be checked
        if not any(a[2] == current_addon_title for a in addons_to_check):
            addons_to_check.append(current_addon_main)
        installed_table = get_user_library_titles(db, user_id, status='installed')
        not_installed = [addon for addon in addons_to_check if addon[2] not in installed_table]
        already_installed = [addon[2] for addon in addons_to_check if addon[2] in installed_table]

        if not not_installed: return jsonify({"dialog": {"title": "All Installed",
                                                         "text": "All required addons are already installed.",
                                                         "buttons": ["Close"]}})

        dialog_text = "None of the required addons are installed."
        button_text = "Install All"
        if already_installed:
            dialog_text = f"Already installed: {', '.join(already_installed)}."
            button_text = "Install the Rest"

        return jsonify({"next_step": "install", "addons_to_install": not_installed,
                        "dialog": {"title": "Library Check", "text": dialog_text, "buttons": [button_text, "Cancel"]}})

    # Case 4: Final Install
    if step == 'install':
        addons_to_install = data.get('addons_to_install', [])
        seen_titles = set()
        unique_addons = []
        for a in addons_to_install:
            title = a[2]  # Addons table: index 2 is title
            if title not in seen_titles:
                seen_titles.add(title)
                unique_addons.append(a)
        addons_to_install = unique_addons
        table_name = f"user_library_{user_id}"

        #Create a list to hold all the download URLs.
        download_urls = []
        #Loop through every addon that is part of the installation.
        for addon_data in addons_to_install:
            title = addon_data[2]
            # Update the database records
            date_installed=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
            existing_record = db.search_one(f"SELECT id FROM {table_name} WHERE title = ?", (title,))
            if existing_record:
                db.run_save(f"UPDATE {table_name} SET status = 'installed', date_installed = ? WHERE title = ?",
                            (date_installed, title))
            else:
                db.run_save(
                    f"INSERT INTO {table_name} (title, category, version, min_msfs_version, date_added, date_installed, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (title, addon_data[6], addon_data[7], addon_data[8], date_installed, date_installed, 'installed'))
            db.run_save("UPDATE Addons SET download_count = download_count + 1 WHERE title = ?", (title,))

            #Get the filename for this specific addon and add its URL to our list
            filename = addon_data[4]
            if filename:
                download_urls.append(url_for('download_addon', filename=filename))

        db.close()

        #Return the complete list of download URLs to the frontend
        seen = set()
        download_urls = [u for u in download_urls if not (u in seen or seen.add(u))]
        return jsonify({
            "status": "success",
            "message": "All required addons are installed successfully!",
            "download_urls": download_urls
        })

    db.close()
    return jsonify({"error": "Invalid step"}), 400

@app.route('/simple_update_library', methods=['POST'])
def simple_update_library():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    action = data.get('action')
    user_library_id = data.get('addon_id')
    user_id = session['user_id']
    table_name = f"user_library_{user_id}"
    db = Database_Manager('flightsim_db.sql')

    if action in ["remove", "uninstall"]:
        db.run_save(f"DELETE FROM {table_name} WHERE id = ?", (user_library_id,))
        db.close()
        return jsonify({"status": "removed"})

    db.close()
    return jsonify({"error": "Invalid simple action"}), 400

@app.route('/download/<filename>')
def download_addon(filename):
    return send_from_directory('static/uploads', filename, as_attachment=True)

@app.route('/aircraft_comparison')
def aircraft_comparison():
    if 'user_id' not in session:
        return redirect('/login')

    db = Database_Manager('flightsim_db.sql')
    aircraft_names_tuples = db.search_all("SELECT name FROM Aircrafts ORDER BY name ASC", values=())
    aircraft_names = [item[0] for item in aircraft_names_tuples]

    stats_query = """
        SELECT 
            MIN(max_speed), MAX(max_speed),
            MIN(mtow), MAX(mtow),
            MIN(fuel_capacity), MAX(fuel_capacity),
            MIN(range), MAX(range),
            MIN(climb_rate), MAX(climb_rate)
        FROM Aircrafts
    """
    stats = db.search_one(stats_query, values=())
    db.close()

    if stats and stats[0] is not None:
        min_max_data = {
            "maxSpeed": {"min": stats[0], "max": stats[1]},
            "mtow": {"min": stats[2], "max": stats[3]},
            "fuelCapacity": {"min": stats[4], "max": stats[5]},
            "range": {"min": stats[6], "max": stats[7]},
            "climbRate": {"min": stats[8], "max": stats[9]}  # UPDATED
        }
    else:
        min_max_data = {
            "maxSpeed": {"min": 0, "max": 0}, "mtow": {"min": 0, "max": 0},
            "fuelCapacity": {"min": 0, "max": 0}, "range": {"min": 0, "max": 0},
            "climbRate": {"min": 0, "max": 0}  # UPDATED
        }

    return render_template('aircraft_comparison.html', aircrafts=aircraft_names, min_max_data=min_max_data)

@app.route('/get_aircraft_data/<string:aircraft_name>')
def get_aircraft_data(aircraft_name):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = Database_Manager('flightsim_db.sql')
    query = """
        SELECT name, image_filename, max_speed, mtow, fuel_capacity, range, climb_rate 
        FROM Aircrafts 
        WHERE name = ?
    """
    data = db.search_one(query, values=(aircraft_name,))
    db.close()

    if data:
        aircraft_data = {
            "name": data[0],
            "imageFilename": data[1],
            "maxSpeed": data[2],
            "mtow": data[3],
            "fuelCapacity": data[4],
            "range": data[5],
            "climbRate": data[6]
        }
        return jsonify(aircraft_data)
    else:
        return jsonify({"error": "Aircraft not found"}), 404

@app.route('/developer_main')
def developer_main():
    if 'user_id' not in session or session.get('role') != 'developer':
        return redirect('/login')

    user_id = session['user_id']
    username = session['username']
    table_name = f"developer_library_{user_id}"

    db = Database_Manager('flightsim_db.sql')

    query = f"""
        SELECT id, title, version, required_for, dependent_on, proposed_date, approved_date, status 
        FROM {table_name} 
        ORDER BY id DESC
    """
    submissions_raw = db.search_all(query, values=())

    submissions_processed = []
    for sub in submissions_raw:
        sub_list = list(sub)
        dependent_on_str = sub_list[4]  # The 'A001:1.0.0' string

        #If there is a dependency string, translate it to a title
        if dependent_on_str:
            #Extract the addon_id part before the colon
            dependency_id = dependent_on_str.split(':')[0]
            #Look up the title for that addon_id
            title_record = db.search_one("SELECT title FROM Addons WHERE addon_id = ?", (dependency_id,))
            if title_record:
                #Replace the ID string with the human-readable title
                sub_list[4] = title_record[0]
            else:
                #If for some reason the addon was deleted, show the ID as a fallback
                sub_list[4] = dependent_on_str

        submissions_processed.append(sub_list)
    db.close()
    return render_template('developer_main.html', username=username, submissions=submissions_processed)

@app.route('/propose_addon', methods=['GET', 'POST'])
def propose_addon():
    if 'user_id' not in session or session.get('role') != 'developer':
        return redirect('/login')

    db = Database_Manager('flightsim_db.sql')
    error = None

    if request.method == 'POST':
        user_id = session['user_id']
        table_name = f"developer_library_{user_id}"

        #Get all form data
        title = request.form.get('title')
        description = request.form.get('description')
        version = request.form.get('version')
        min_msfs_version = request.form.get('min_msfs_version')
        category = request.form.get('category')

        dependent_on_title = request.form.get('dependent_on')
        required_for_title = request.form.get('required_for')

        # 1.Format the 'dependent_on' value
        dependent_on_formatted = None  # Default to None (for NULL)
        if dependent_on_title:  # If a selection was made
            dependency_addon = db.search_one("SELECT addon_id, version FROM Addons WHERE title = ?",
                                             (dependent_on_title,))
            if dependency_addon:
                addon_id, addon_version = dependency_addon
                dependent_on_formatted = f"{addon_id}:{addon_version}"

        # 2.Format the 'required_for' value (this is just the title, as per your description)
        required_for_formatted = required_for_title if required_for_title else None

        #Backend validation
        allowed_msfs_versions = ['1.20', '1.21', '1.22', '1.23', '1.24', '1.25', '1.26', '1.27', '1.28', '1.29', '1.30']
        version_pattern = re.compile(r"^\d+\.\d+\.\d+$")

        if not version_pattern.match(version):
            error = "Invalid format for Version. Please use a format like '1.0.0'."
        elif min_msfs_version not in allowed_msfs_versions:
            error = "Invalid Minimum MSFS Version selected."
        else:
            existing_addon = db.search_one("SELECT id FROM Addons WHERE title = ?", (title,))
            if existing_addon:
                error = f"An addon with the title '{title}' already exists."
            else:
                image_file = request.files.get('image_file')
                model_file = request.files.get('model_file')
                if not image_file or not model_file:
                    error = "Both an image and a zip file are required."
                else:
                    image_filename = secure_filename(image_file.filename)
                    model_filename = secure_filename(model_file.filename)
                    upload_path = 'static/proposals'
                    os.makedirs(upload_path, exist_ok=True)
                    image_file.save(os.path.join(upload_path, image_filename))
                    model_file.save(os.path.join(upload_path, model_filename))

                    # 3.Use the new formatted dependency values in the insert statement
                    insert_query = f"""
                        INSERT INTO {table_name} (
                            title, description, model_filename, image_filename, category,
                            version, min_msfs_version, dependent_on, required_for,
                            proposed_date, approved_date, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    db.run_save(insert_query, values=(
                        title, description, model_filename, image_filename, category,
                        version, min_msfs_version, dependent_on_formatted, required_for_formatted,
                        (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), None, 'awaiting'
                    ))
                    db.close()
                    return redirect(url_for('developer_main'))

    #GET request part
    all_addons = [row[0] for row in db.search_all("SELECT title FROM Addons ORDER BY title ASC", values=())]
    no_dependency_addons_query = "SELECT title FROM Addons WHERE dependency IS NULL OR dependency = '' OR dependency = '{}' ORDER BY title ASC"
    no_dependency_addons = [row[0] for row in db.search_all(no_dependency_addons_query, values=())]
    db.close()
    return render_template('propose_addon.html', all_addons=all_addons, no_dependency_addons=no_dependency_addons,
                           error=error)

@app.route('/admin_main')
def admin_main():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    return render_template('admin_main.html', username=session.get('username'))

@app.route('/admin_users')
def admin_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    db = Database_Manager('flightsim_db.sql')
    users = db.search_all(
        "SELECT user_id, first_name, last_name, preferred_username, email, msfs_version FROM Users WHERE role = 'user'",
        values=())
    db.close()

    return render_template('admin_users.html', users=users)

@app.route('/remove_user/<int:user_id>', methods=['POST'])
def remove_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    db = Database_Manager('flightsim_db.sql')
    db.run_save("DELETE FROM Users WHERE user_id = ?", values=(user_id,))
    db.run_save(f"DROP TABLE IF EXISTS user_library_{user_id}", values=())
    db.close()

    return redirect(url_for('admin_users'))

@app.route('/admin_developers')
def admin_developers():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = Database_Manager('flightsim_db.sql')
    developers = db.search_all(
        "SELECT user_id, first_name, last_name, preferred_username, email FROM Users WHERE role = 'developer'",
        values=())
    db.close()

    return render_template('admin_developers.html', developers=developers)

@app.route('/developer_library/<int:dev_id>')
def view_developer_library(dev_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = Database_Manager('flightsim_db.sql')
    dev_info = db.search_one("SELECT preferred_username FROM Users WHERE user_id = ?", (dev_id,))
    if not dev_info:
        return "Developer not found", 404

    table_name = f"developer_library_{dev_id}"
    proposed = db.search_all(f"SELECT * FROM {table_name} WHERE status = 'awaiting'", values=())
    approved = db.search_all(f"SELECT * FROM {table_name} WHERE status = 'approved'", values=())
    db.close()

    return render_template('admin_view_developer_library.html', proposed=proposed, approved=approved, dev_id=dev_id,
                           developer_name=dev_info[0])

@app.route('/handle_submission/<int:dev_id>/<int:sub_id>/<string:action>', methods=['POST'])
def handle_submission(dev_id, sub_id, action):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    dev_table = f"developer_library_{dev_id}"
    db = Database_Manager('flightsim_db.sql')
    submission = db.search_one(f"SELECT * FROM {dev_table} WHERE id = ?", (sub_id,))

    if not submission:
        db.close()
        return "Submission not found", 404

    model_filename = submission[3]
    image_filename = submission[4]

    if action == 'approve':
        #Addon ID generation
        category = submission[5]
        count_query = "SELECT COUNT(*) FROM Addons WHERE category = ?"
        count_result = db.search_one(count_query, (category,))
        existing_count = count_result[0] if count_result else 0
        new_sequential_number = existing_count + 1
        category_prefix = category[0].upper()
        formatted_number = f"{new_sequential_number:03d}"
        new_addon_id = f"{category_prefix}{formatted_number}"

        dev_info = db.search_one("SELECT preferred_username FROM Users WHERE user_id = ?", (dev_id,))
        developer_name = dev_info[0] if dev_info else "Unknown"

        shutil.move(f'static/proposals/{model_filename}', f'static/uploads/{model_filename}')
        shutil.move(f'static/proposals/{image_filename}', f'static/{image_filename}')

        #Insert the new addon with its direct dependency (from 'dependent_on' field)
        insert_query = """
            INSERT INTO Addons (
                addon_id, title, description, model_filename, image_filename, category, 
                version, min_msfs_version, dependency, developer, uploader_id, download_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.run_save(insert_query, values=(
            new_addon_id, submission[1], submission[2], model_filename, image_filename, category,
            submission[6], submission[7], submission[8], developer_name, dev_id, 0
        ))

        #Get the title of the addon that this new addon is required for.
        required_for_title = submission[9]

        if required_for_title:
            #1.Find the target addon in the main Addons table.
            target_addon = db.search_one("SELECT id FROM Addons WHERE title = ?", (required_for_title,))

            if target_addon:
                target_id = target_addon[0]
                #2.Create the simple dependency string: "A004:1.0.0"
                new_dependency_string = f"{new_addon_id}:{submission[6]}"
                #3.Update the target addon's 'dependency' column with this simple string.
                #This overwrites any previous value, which is correct since the UI only shows addons with no dependency in the "Required For" dropdown
                db.run_save("UPDATE Addons SET dependency = ? WHERE id = ?", (new_dependency_string, target_id))

        #Update the submission status in the developer's library
        db.run_save(f"UPDATE {dev_table} SET status = 'approved', approved_date = ? WHERE id = ?",
                    values=((datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), sub_id))

    elif action == 'decline':
        os.remove(f'static/proposals/{model_filename}')
        os.remove(f'static/proposals/{image_filename}')
        db.run_save(f"UPDATE {dev_table} SET status = 'declined' WHERE id = ?", values=(sub_id,))
    db.close()
    return redirect(request.referrer)

@app.route('/admin_addons')
def admin_addons():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    db = Database_Manager('flightsim_db.sql')
    all_proposed = []
    developers = db.search_all("SELECT user_id, preferred_username FROM Users WHERE role = 'developer'", values=())
    for dev in developers:
        dev_id, dev_name = dev
        dev_table = f"developer_library_{dev_id}"
        proposed_from_dev = db.search_all(f"SELECT * FROM {dev_table} WHERE status = 'awaiting'", values=())
        for prop in proposed_from_dev:
            all_proposed.append(list(prop) + [dev_name, dev_id])

    approved_query = "SELECT * FROM Addons ORDER BY id DESC"
    all_approved = db.search_all(approved_query, values=())
    db.close()

    return render_template('admin_addons.html', proposed=all_proposed, approved=all_approved)

@app.route('/remove_addon_by_title', methods=['POST'])
def remove_addon_by_title():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    #Get the title from the hidden input in the form
    addon_title = request.form.get('title')
    if not addon_title:
        return "Missing addon title", 400
    db = Database_Manager('flightsim_db.sql')
    #1.Find the addon in the main Addons table by its UNIQUE title
    addon_to_remove = db.search_one("SELECT * FROM Addons WHERE title = ?", (addon_title,))
    if not addon_to_remove:
        db.close()
        #This can happen if it was already deleted, so we just redirect
        return redirect(request.referrer)

    #Unpack the necessary data using the correct indices
    addon_id = addon_to_remove[0]  #The main Addons table primary key
    model_filename = addon_to_remove[4]
    image_filename = addon_to_remove[5]
    developer_name = addon_to_remove[10]

    #2.Find the developer's ID and delete from their personal library
    dev_info = db.search_one("SELECT user_id FROM Users WHERE preferred_username = ?", (developer_name,))
    if dev_info:
        dev_id = dev_info[0]
        dev_table = f"developer_library_{dev_id}"
        db.run_save(f"DELETE FROM {dev_table} WHERE title = ?", (addon_title,))

    #3.Delete from the main Addons table using its primary key
    db.run_save("DELETE FROM Addons WHERE id = ?", (addon_id,))

    #4.Delete the files
    if os.path.exists(f'static/uploads/{model_filename}'): os.remove(f'static/uploads/{model_filename}')
    if os.path.exists(f'static/{image_filename}'): os.remove(f'static/{image_filename}')

    #5.Cascade delete from all user libraries
    all_users = db.search_all("SELECT user_id FROM Users WHERE role = 'user'", values=())
    for user in all_users:
        user_table = f"user_library_{user[0]}"
        db.run_save(f"DELETE FROM {user_table} WHERE title = ?", (addon_title,))

    db.close()
    return redirect(request.referrer)  #redirect back to the page the admin was on

if __name__ == '__main__':
    app.run(debug=True)
