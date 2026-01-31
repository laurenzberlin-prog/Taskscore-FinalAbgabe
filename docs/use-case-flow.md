# Use Case Flow – TaskScore (pro Screen)

```mermaid
flowchart TD

%% ENTRY
A[Browser öffnet App] --> B{Session user_id vorhanden?}

B -- Nein --> L[Login Screen<br>/login (GET)]
B -- Ja --> H[Home Screen<br>/ (GET)]

%% LOGIN
L --> L1[User gibt Username + Passwort ein]
L1 --> L2[Login absenden<br>/login (POST)]
L2 --> L3{Credentials gültig?}
L3 -- Nein --> L4[Fehlermeldung anzeigen<br>Login fehlgeschlagen]
L4 --> L
L3 -- Ja --> L5[Session setzen<br>session['user_id'] = user_id]
L5 --> H

%% REGISTER
L --> R[Register Screen<br>/register (GET)]
R --> R1[User gibt Username + Passwort ein]
R1 --> R2[Registrierung absenden<br>/register (POST)]
R2 --> R3{Username frei + Passwort ok?}
R3 -- Nein --> R4[Fehlermeldung anzeigen]
R4 --> R
R3 -- Ja --> R5[User anlegen in DB]
R5 --> L

%% HOME
H --> N1[Navigation: Tasks]
H --> N2[Navigation: Weekly Plan]
H --> N3[Navigation: Progress]
H --> O[Logout<br>/logout (GET)]

O --> O1[Session löschen<br>session.pop('user_id')]
O1 --> L

%% TASKS SCREEN
N1 --> T[Tasks Screen<br>/tasks (GET)]
T --> T1[Neue Aufgabe ausfüllen]
T1 --> T2[Aufgabe speichern<br>/tasks (POST)]
T2 --> T3{Budget überschritten?}
T3 -- Ja --> T4[Fehlermeldung anzeigen]
T4 --> T
T3 -- Nein --> T5[Task in DB speichern (user_id)]
T5 --> T

T --> T6[Task als DONE/OPEN toggeln]
T6 --> T7[/tasks/<id>/toggle (POST)]
T7 --> T8[Status ändern + ggf. Score erhöhen]
T8 --> T

T --> T9[Task löschen]
T9 --> T10[/tasks/<id>/delete (POST)]
T10 --> T11[Task löschen (nur eigener user_id)]
T11 --> T

%% WEEKLY PLAN SCREEN
N2 --> P[Weekly Plan Screen<br>/plan (GET)]
P --> P1[Wochenpunkte pro Tag laden (nur user_id)]
P1 --> P

%% PROGRESS SCREEN
N3 --> G[Progress Screen<br>/progress (GET)]
G --> G1[Total Points + Done Points laden (nur user_id)]
G1 --> G

%% AUTH GUARD (vereinfachte Darstellung)
T -->|wenn nicht eingeloggt| L
P -->|wenn nicht eingeloggt| L
G -->|wenn nicht eingeloggt| L
H -->|wenn nicht eingeloggt| L