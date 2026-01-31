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
...

Beschreibung der Entitäten

Im Datenmodell der Anwendung TaskScore existieren drei zentrale Entitäten: User, Task und Stats.
Diese Entitäten bilden die Grundlage für die Speicherung von Benutzern, Aufgaben und globalen Statistikwerten.

User

Die Entität User repräsentiert einen registrierten Benutzer der Anwendung.
Jeder User besitzt:
	•	eine eindeutige ID (id)
	•	einen Benutzernamen (username)
	•	einen Passwort-Hash (password_hash)

Der Passwort-Hash wird mit Hilfe der Bibliothek werkzeug.security erzeugt und gespeichert, sodass niemals Klartext-Passwörter in der Datenbank abgelegt werden.
Der Benutzername ist eindeutig und dient als Login-Identifikator.

Task

Die Entität Task repräsentiert eine einzelne Aufgabe innerhalb des Wochenplans eines Benutzers.
Jede Aufgabe besitzt folgende Attribute:
	•	id: eindeutige Identifikation der Aufgabe
	•	title: Titel der Aufgabe
	•	description: optionale Beschreibung
	•	weekday: zugeordneter Wochentag
	•	points_total: Punktwert der Aufgabe
	•	status: Status (OPEN oder DONE)
	•	rewarded: Flag, ob die Aufgabe bereits zur Statistik gezählt wurde
	•	user_id: Fremdschlüssel auf den Benutzer

Über das Attribut user_id ist jede Aufgabe eindeutig einem User zugeordnet.
Dadurch wird sichergestellt, dass jeder Benutzer ausschließlich seine eigenen Aufgaben sehen und bearbeiten kann.

Das Feld rewarded verhindert, dass beim mehrfachen Umschalten einer Aufgabe von OPEN zu DONE der Score mehrfach erhöht wird.