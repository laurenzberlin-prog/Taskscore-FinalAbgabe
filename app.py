from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import *

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"
init_db()

BUDGET = 100


@app.route("/")
def start():
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]

    return render_template(
        "home.html",
        current_total=get_total_points(uid),
        budget=BUDGET,
        done_score=get_done_task_count(uid)
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
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    error = None

    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description")
        weekday = request.form["weekday"]
        points = int(request.form.get("points_total") or 0)
        total = get_total_points(uid)

        if total + points <= BUDGET:
            insert_task(title, description, weekday, points, uid)
            return redirect(url_for("show_tasks"))

        error = f"Wochenbudget überschritten ({total + points}/{BUDGET})"

    return render_template(
        "tasks.html",
        tasks=get_all_tasks(uid),
        current_total=get_total_points(uid),
        budget=BUDGET,
        error=error
    )


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    toggle_task_status(task_id, uid)
    return redirect(url_for("show_tasks"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task_route(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    delete_task(task_id, uid)
    return redirect(url_for("show_tasks"))


@app.route("/plan")
def weekly_plan():
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    return render_template("plan.html", weekly_points=get_weekly_points(uid))


@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect(url_for("login"))

    uid = session["user_id"]
    return render_template(
        "progress.html",
        total_points=get_total_points(uid),
        done_points=get_done_points(uid)
    )


@app.route("/api/status")
def api_status():
    if "user_id" not in session:
        return jsonify({"error": "not logged in"})

    uid = session["user_id"]
    return jsonify({
        "budget": BUDGET,
        "current_total": get_total_points(uid),
        "done_points": get_done_points(uid),
        "done_score": get_done_task_count(uid),
        "task_count": len(get_all_tasks(uid))
    })


if __name__ == "__main__":
    app.run(debug=True)