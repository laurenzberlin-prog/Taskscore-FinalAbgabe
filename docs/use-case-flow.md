# Use Case Flow – TaskScore (pro Screen)

```mermaid
flowchart TD

%% ENTRY
A[Browser öffnet App] --> B{Session user_id vorhanden?}
B -- Nein --> L[Login Screen\nGET /login\nrender_template('login.html')]
B -- Ja --> H[Home Screen\nGET /\nrender_template('home.html')]

%% LOGIN SCREEN
L --> L1[User gibt username + password ein]
L1 --> L2[POST /login]
L2 --> L3[verify_user(username, password)\n(database.py)]
L3 -->|ok -> user_id| L4[session['user_id']=user_id]
L4 --> H
L3 -->|None| L5[error='Login fehlgeschlagen'\nrender login.html]

%% REGISTER SCREEN
L --> R0[Link: Registrieren]
R0 --> R[Register Screen\nGET /register\nrender_template('register.html')]
R --> R1[User wählt username + password]
R1 --> R2[POST /register]
R2 --> R3[create_user(username, password)\n(database.py)]
R3 -->|ok| L
R3 -->|fail| R4[error z.B. 'Name vergeben'\nrender register.html]

%% HOME SCREEN
H --> H1[Home zeigt Budget-Status\nget_total_points(user_id)]
H --> H2[Home zeigt TaskScore\nget_done_task_count(user_id)]
H --> NAV{Navigation}

NAV --> T[Tasks Screen\nGET /tasks\nget_all_tasks(user_id)\nrender 'tasks.html']
NAV --> P[Plan Screen\nGET /plan\nget_weekly_points(user_id)\nrender 'plan.html']
NAV --> PR[Progress Screen\nGET /progress\nget_total_points(user_id)\nget_done_points(user_id)\nrender 'progress.html']
NAV --> LO[Logout\nGET /logout\nsession.pop('user_id')\nredirect /login]

%% TASKS SCREEN ACTIONS
T --> T1[Form: Neue Task]
T1 --> T2[POST /tasks]
T2 --> T3[get_total_points(user_id)]
T3 --> T4{Budget ok? total+points <= 100}
T4 -- Ja --> T5[insert_task(..., user_id)]
T5 --> T
T4 -- Nein --> T6[error='Wochenbudget überschritten'\nrender tasks.html]

T --> T7[Button: Status toggle]
T7 --> T8[POST /tasks/<id>/toggle]
T8 --> T9[toggle_task_status(task_id, user_id)]
T9 --> T

T --> T10[Button: Löschen]
T10 --> T11[POST /tasks/<id>/delete]
T11 --> T12[delete_task(task_id, user_id)]
T12 --> T

%% PLAN SCREEN
P --> P1[Zeigt Tabelle weekly_points\n(Jinja loop)]
P1 --> NAV

%% PROGRESS SCREEN
PR --> PR1[berechnet percent\n(done_points / total_points * 100)]
PR1 --> NAV