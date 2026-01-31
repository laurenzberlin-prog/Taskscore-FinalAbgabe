# Data Model (UML) – TaskScore

Dieses UML-Diagramm beschreibt die Datenstruktur der Anwendung TaskScore.  
Es basiert auf der SQLite-Datenbank (`taskscore.db`) und zeigt die zentralen Entitäten sowie deren Beziehungen.

## UML Diagramm

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
