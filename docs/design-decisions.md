# Design Decisions – TaskScore

Diese Datei dokumentiert zentrale technische und konzeptionelle Entscheidungen während der Entwicklung.

---

## 1. Entscheidung: Punktesystem statt Zeitangaben

**Problem:**  
Zeitangaben sind subjektiv und schwer einzuschätzen.

**Lösung:**  
Ein einfaches Punktesystem (0–100 pro Woche).

**Begründung:**  
Punkte sind flexibler, leichter verständlich und zwingen zur Priorisierung.

---

## 2. Entscheidung: Kein externes Frontend (React etc.)

**Problem:**  
Zusätzliche Komplexität ohne Mehrwert.

**Lösung:**  
Reines Server-Side-Rendering mit Jinja2.

**Begründung:**  
- Einfacher Debug
- Kein Build-System
- Klarer HTML-Flow

---

## 3. Entscheidung: User-System mit Session

**Problem:**  
Mehrere Nutzer sollen getrennte Aufgaben haben.

**Lösung:**  
Session-basierte Authentifizierung mit SQLite.

**Begründung:**  
- Keine externe Abhängigkeit
- Für lokale Demo ausreichend
- Klar nachvollziehbar


---

## 6. Entscheidung: Bewusst simples UI

**Problem:**  
Zu viele Features führen zu kognitiver Überlastung.

**Lösung:**  
Reduziertes UI mit Cards und klarer Navigation.

**Begründung:**  
Fokus liegt auf Funktion, nicht auf Design-Spielereien.

---

## 7. Entscheidung: Kein automatisches Speichern

**Problem:**  
Komplexere Zustandsverwaltung nötig.

**Lösung:**  
Explizite Buttons (Submit / Toggle / Delete).

**Begründung:**  
- Nutzerkontrolle
- Weniger Bugs
- Klarer Request-Flow

---

## Zusammenfassung

Alle Designentscheidungen folgen drei Prinzipien:

1. **Einfachheit**
2. **Nachvollziehbarkeit**
3. **Lehrbarkeit**

Das Projekt wurde bewusst nicht „over-engineered“, sondern so umgesetzt,  
dass jede Funktion logisch erklärbar ist.