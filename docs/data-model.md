# Data Model & Use Case Model – TaskScore

## Data Model (UML)

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


'## Use Case Model'
flowchart LR

User((User))

Login[Login]
Register[Register]
AddTask[Create Task]
DeleteTask[Delete Task]
ViewTasks[View Tasks]
ToggleTask[Mark Task as Done]
ViewPlan[View Weekly Plan]
ViewProgress[View Progress]
Logout[Logout]

User --> Login
User --> Register
User --> AddTask
User --> DeleteTask
User --> ViewTasks
User --> ToggleTask
User --> ViewPlan
User --> ViewProgress
User --> Logout