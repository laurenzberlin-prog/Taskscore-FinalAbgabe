from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import (
    init_db,verify_user,create_user,get_total_points,get_user_done_score,get_all_tasks,insert_task,toggle_task_status,delete_task,get_weekly_points,get_done_points,
)

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

BUDGET = 100
init_db()


def require_login():
    return "user_id" in session


@app.route("/")
def start():
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    return render_template(
        "home.html",
        current_total=get_total_points(uid),
        budget=BUDGET,
        done_score=get_user_done_score(uid),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = verify_user(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect(url_for("start"))

        error = "Login fehlgeschlagen."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ok, msg = create_user(username, password)
        if ok:
            return redirect(url_for("login"))
        error = msg

    return render_template("register.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/tasks", methods=["GET", "POST"])
def show_tasks():
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    error = None

    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description")
        points = int(request.form.get("points_total") or 0)

    
        weekdays = request.form.getlist("weekdays")

        if not weekdays:
            error = "Bitte mindestens einen Wochentag auswählen."
        else:
            total = get_total_points(uid)
            needed = points * len(weekdays)

            if total + needed <= BUDGET:
                for day in weekdays:
                    insert_task(title, description, day, points, uid)
                return redirect(url_for("show_tasks"))
            else:
                error = f"Wochenbudget überschritten ({total + needed}/{BUDGET})"

    return render_template(
        "tasks.html",
        tasks=get_all_tasks(uid),
        current_total=get_total_points(uid),
        budget=BUDGET,
        error=error,
    )


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    toggle_task_status(task_id, uid)
    return redirect(url_for("show_tasks"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task_route(task_id):
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    delete_task(task_id, uid)
    return redirect(url_for("show_tasks"))


@app.route("/plan")
def weekly_plan():
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    return render_template("plan.html", weekly_points=get_weekly_points(uid))


@app.route("/progress")
def progress():
    if not require_login():
        return redirect(url_for("login"))

    uid = session["user_id"]
    return render_template(
        "progress.html",
        total_points=get_total_points(uid),
        done_points=get_done_points(uid),
    )


@app.route("/api/status")
def api_status():
    if not require_login():
        return jsonify({"error": "not logged in"})

    uid = session["user_id"]
    return jsonify(
        {
            "budget": BUDGET,
            "current_total": get_total_points(uid),
            "done_points": get_done_points(uid),
            "done_score": get_user_done_score(uid),
            "task_count": len(get_all_tasks(uid)),
        }
    )

if __name__ == "__main__":
    app.run(debug=True)