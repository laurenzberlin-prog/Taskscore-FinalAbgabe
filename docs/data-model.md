# Data Model (UML) – TaskScore

Dieses UML-Diagramm beschreibt die Datenstruktur der Anwendung TaskScore.  
Es basiert auf der SQLite-Datenbank (`taskscore.db`) und zeigt die zentralen Entitäten sowie deren Beziehungen.

## UML Diagramm

```mermaid
classDiagram
direction LR

class User {
  +int id
  +string username
  +string password_hash
}

class Task {
  +int id
  +string title
  +string description
  +string weekday
  +int points_total
  +string status
  +int rewarded
  +int user_id
}

class Stats {
  +int id
  +int done_score
}

User "1" --> "0..*" Task : owns
Stats "1" --> "0..*" Task : counts done

Beschreibung der Entitäten

Im Datenmodell der Anwendung TaskScore existieren drei zentrale Entitäten: User, Task und Stats. Diese Entitäten bilden die Grundlage für die Speicherung von Benutzern, Aufgaben und globalen Statistikwerten.

Die Entität User repräsentiert einen registrierten Benutzer der Anwendung. Jeder User besitzt eine eindeutige ID, einen Benutzernamen sowie einen Passwort-Hash. Der Passwort-Hash wird mit Hilfe der Bibliothek werkzeug.security erzeugt und gespeichert, sodass niemals Klartext-Passwörter in der Datenbank abgelegt werden. Der Benutzername ist eindeutig und dient als Login-Identifikator.

Die Entität Task repräsentiert eine einzelne Aufgabe innerhalb des Wochenplans eines Benutzers. Jede Aufgabe besitzt eine eindeutige ID, einen Titel, eine optionale Beschreibung, einen zugeordneten Wochentag, eine Punktzahl (points_total), einen Status (OPEN oder DONE), ein Reward-Flag sowie eine Benutzer-ID. Über die Benutzer-ID ist jede Aufgabe eindeutig einem User zugeordnet. Dadurch wird sichergestellt, dass jeder Benutzer ausschließlich seine eigenen Aufgaben sehen und bearbeiten kann.

Das Feld rewarded dient dazu, zu speichern, ob eine Aufgabe bereits zur Erhöhung des Done-Scores gezählt wurde. Dadurch wird verhindert, dass beim mehrfachen Umschalten einer Aufgabe von OPEN zu DONE der Score mehrfach erhöht wird.

Die Entität Stats speichert globale Statistikwerte der Anwendung. Aktuell wird hier lediglich der Wert done_score gespeichert, welcher die Gesamtanzahl aller jemals erledigten Aufgaben über alle Benutzer hinweg zählt. Diese Tabelle besitzt bewusst nur einen einzigen Datensatz mit der festen ID 1 und dient als einfache globale Statistik ohne Benutzerbezug.


Beziehungen zwischen den Entitäten

Zwischen den Entitäten bestehen folgende Beziehungen:
	•	Ein User kann beliebig viele Tasks besitzen.
	•	Jede Task gehört genau zu einem User.

Diese Beziehung wird über das Attribut user_id in der Task-Tabelle realisiert, welches auf die ID eines Users verweist.

Zwischen Task und Stats besteht keine direkte relationale Verbindung. Die Stats-Tabelle wird ausschließlich programmatisch aktualisiert, wenn eine Aufgabe erstmalig auf den Status DONE gesetzt wird.