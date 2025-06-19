from flask import Flask, render_template, redirect, url_for, request, flash, session
import db_manager, bot_runner, multiprocessing, json
running_bots = {}
app = Flask(__name__)
app.secret_key = "SKIBIDI"

Real_username = "Sigma"
Real_password = "skibidi"


db_manager.initiate_db()

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db_manager.Login(username, password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash('Wrong password or username.')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db_manager.Check_taken(username):
            flash('This username is taken')
            return redirect(url_for('signup'))
        db_manager.Add_user(username, password)
        flash('You have successfuly signed up, login.')
        return redirect(url_for('login'))
    return render_template("signup.html")

def Login_checker():
    if 'username' not in session:
        flash('You have to log in first!')
        return True


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if Login_checker():
        return redirect(url_for("login"))
    if request.method == "POST":
        if request.form.get("run"):
            if not session['username'] in running_bots.keys():
                bot_token = db_manager.Fetch_data(session['username'], 3)
                responces = json.loads(db_manager.Fetch_data(session['username'], 4))
                commands = json.loads(db_manager.Fetch_data(session['username'], 5))
                config = json.loads(db_manager.Fetch_data(session['username'], 6))
                running_bots[session['username']] = multiprocessing.Process(target=bot_runner.New_bot, args=(bot_token, config, responces, commands))
                running_bots[session['username']].start()
            else:
                flash("Your bot is already running!")
    return render_template("dashboard.html", username=session['username'])

@app.route("/logout")
def logout():
    if running_bots[session['username']]:
        running_bots[session['username']].terminate()
        del running_bots[session['username']]
    session.pop('username', None)
    flash('Logged out successfuly.')
    return redirect(url_for('home'))

@app.route("/token", methods=["POST", "GET"])
def token():
    if Login_checker():
        return redirect(url_for("login"))
    if request.method == "POST":
        token = request.form.get("token")
        db_manager.Update_db(session['username'], "token", token)
    return render_template("token.html", token=db_manager.Fetch_data(session['username'], 3))


@app.route("/responces", methods=["POST", "GET"])
def responces():
    if Login_checker():
        return redirect(url_for("login"))
    responces = json.loads(db_manager.Fetch_data(session['username'], 4))
    if request.method == "POST":
        num_responces = int(request.form.get("num_responces"))
        if request.form.get("Update"):
            temp_dict = {}
            for i in range(num_responces):
                if num_responces == 69:
                    temp_dict[f"Bad 69 joke nr{i}"] = "Bad 69 joke"
                    continue
                try:
                    if_message = request.form.get(f"if_mess{i}")
                    responce = request.form.get(f"resp{i}")
                    temp_dict[if_message] = responce
                except:
                    continue
            db_manager.Update_db(session['username'], "responces", json.dumps(temp_dict))
            return render_template("responces.html", num_responces=num_responces, responces=temp_dict, dict_len=len(responces.keys()))
        return render_template("responces.html", num_responces=num_responces, responces=responces, dict_len=len(responces.keys()))
    else:
        return render_template("responces.html", num_responces=len(responces.keys()), responces=responces, dict_len=len(responces.keys()))


@app.route("/commands", methods=["POST", "GET"])
def commands():
    if Login_checker():
        return redirect(url_for("login"))
    commands = json.loads(db_manager.Fetch_data(session['username'], 5))
    if request.method == "POST":
        temp_dict = {}
        temp_dict["Hello"] = request.form.get("hello_cmd")
        temp_dict["Random_num"] = request.form.get("Rand_cmd")
        temp_dict["Date"] = request.form.get("Date_cmd")
        db_manager.Update_db(session['username'], "commands", json.dumps(temp_dict))
        return render_template("commands.html", commands=temp_dict)
    return render_template("commands.html", commands=commands)

@app.route("/config", methods=["POST", "GET"])
def config():
    if Login_checker():
        return redirect(url_for("login"))
    config = json.loads(db_manager.Fetch_data(session['username'], 6))
    if request.method == "POST":
        if len(request.form.get("cmd_prefix")) > 1:
            flash("Command prefix must be a single character")
            return render_template("config.html", config=config)
        temp_dict = {}
        temp_dict["command_prefix"] = request.form.get("cmd_prefix")
        temp_dict["user_replace"] = request.form.get("user_replace")
        temp_dict["bot_replace"] = request.form.get("bot_replace")
        db_manager.Update_db(session['username'], "config", json.dumps(temp_dict))
        return render_template("config.html", config=temp_dict)             
    return render_template("config.html", config=config)

app.run(debug=True)