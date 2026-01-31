# Data Model & Use Case Model – TaskScore

Dieses Dokument beschreibt sowohl die **Datenstruktur (Data Model / UML)** als auch die
**funktionalen Anwendungsfälle (Use Cases)** der Web-Anwendung TaskScore.

---

## 1. Data Model (UML)

Dieses UML-Diagramm beschreibt die Datenstruktur der Anwendung TaskScore.  
Es basiert auf der SQLite-Datenbank (`taskscore.db`) und zeigt die zentralen Entitäten
sowie deren Beziehungen.

### UML Diagramm

```mermaid
classDiagram
direction LR

class User {
  int id
  string username
  string password_hash
}

class Task {
  int id
  string title
  string description
  string weekday
  int points_total
  string status
  int rewarded
  int user_id
}

class Stats {
  int id
  int done_score
}

User "1" --> "0..*" Task : owns


usecaseDiagram
title TaskScore – Use Case Diagramm

actor User as U

rectangle "TaskScore Web-App" {
  (Registrieren)
  (Einloggen)
  (Ausloggen)

  (Startseite ansehen)
  (Aufgaben anzeigen)
  (Aufgabe anlegen)
  (Aufgabe als DONE/OPEN markieren)
  (Aufgabe löschen)

  (Wochenplan ansehen)
  (Fortschritt ansehen)
}

U --> (Registrieren)
U --> (Einloggen)
U --> (Ausloggen)

U --> (Startseite ansehen)
U --> (Aufgaben anzeigen)
U --> (Aufgabe anlegen)
U --> (Aufgabe als DONE/OPEN markieren)
U --> (Aufgabe löschen)
U --> (Wochenplan ansehen)
U --> (Fortschritt ansehen)