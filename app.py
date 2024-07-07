from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import database
import secrets
from datetime import timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/loginPage")
def login_page():
    email = request.args.get('email')
    if email is None:
        email = ""
    return render_template("loginPage.html", email=email)


@app.route("/signUpPage")
def sign_up_page():
    return render_template("signUpPage.html")


@app.route("/createUser", methods=["POST"])
def create_user():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    new_user_status = database.addUser(fname, lname, phone, email, password)
    if new_user_status["status"] == "Success":
        session["email"] = email
        session["user_fname"] = fname
        session["user_lname"] = lname
        session["user_phone"] = phone
        return redirect(url_for("home_page"))
    else:
        flash(new_user_status["message"], "danger")
        return redirect(url_for("sign_up_page"))


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home_page'))


@app.route("/validateUser", methods=['post'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = database.get_user_details(email)
    if password == user[0]["user_password"]:
        session.permanent = True
        session["email"] = email
        session["user_fname"] = user[0]["fname"]
        session["user_lname"] = user[0]["lname"]
        session["user_phone"] = user[0]["user_phone"]
        return redirect(url_for("home_page"))
    else:
        flash("Invalid password", "danger")
        return redirect(url_for("login_page", email=email))


@app.route("/")
def home_page():
    jobs = database.load_jobs_from_db()
    return render_template('home.html', jobs=jobs)


@app.route("/jobs")
def display_jobs():
    jobs = database.load_jobs_from_db()
    return render_template('pages/jobs_page.html', jobs=jobs)


@app.route("/overview")
def get_overview():
    return render_template('pages/overview.html')


@app.route("/jobs/<job_id>")
def get_job_details(job_id):
    job_details = database.get_job_details(job_id)
    if len(job_details) != 0:
        return render_template('pages/job_details.html',
                               job_details=job_details)
    else:
        return "Job Not Found", 404


@app.route("/jobs/<job_id>/apply", methods=['post'])
def apply_to_job(job_id):
    data = request.form
    return data


@app.route("/faqs")
def get_faqs():
    faqs = database.get_faqs_from_db()
    return render_template('pages/faqs.html', faqs=faqs)


##############################################################################
# Api's
##############################################################################
@app.route("/api/job")
def load_job():
    job_id = request.args['job_id']
    job_details = database.get_job_details(job_id)
    return jsonify(job_details)


@app.route("/api/jobs")
def list_jobs():
    jobs = database.load_jobs_from_db()
    return jsonify(jobs)


@app.route("/api/users/<email>")
def list_users(email):
    user_details = database.get_user_details(email)
    return jsonify(user_details)


@app.route("/api/users/byPyhone/<phone>")
def list_users_by_phone(phone):
    try:
        user_details = database.get_user_details_for_phone(phone)
        return jsonify(user_details)
    except:
        return {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
