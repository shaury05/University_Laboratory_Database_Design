# Research Lab Management System

A comprehensive database application designed to streamline the administrative operations of a university research laboratory. This system manages the complex relationships between lab members, grant funding, research projects, equipment usage, and academic publications.

The project demonstrates a full-lifecycle database implementation: from **EER Conceptual Modeling** to **Relational Schema Normalization** and a **Python-based CLI application** layer.

## 🚀 Key Features

* **Member Management:** Tracks a hierarchy of lab members including Faculty, Students (PhD/Masters), and External Collaborators using supertype/subtype relationships.
* **Grant & Project Tracking:** Manages funding sources and their allocation to specific research projects and personnel.
* **Equipment Concurrency Control:** Implements **Application-Level Validation** to enforce business rules that standard SQL constraints cannot handle (e.g., preventing equipment checkout if active users ≥ 3).
* **Recursive Relationships:** Handles internal mentorship programs where lab members mentor other members.
* **Analytical Reporting:** Generates insights such as:
    * Average student publications per major.
    * Active projects filtered by grant and date ranges.
    * Top publishing members.

## 🛠️ Tech Stack

* **Database:** MySQL 9.5
* **Language:** Python 3.x
* **Driver:** `mysql-connector-python`
* **Design Tools:** EER Modeling, Relational Algebra

## 📂 Repository Structure

* `app.py`: The main Python entry point containing the CLI menu and application logic.
* `schema.sql`: DDL scripts to create the database, tables, views, and constraints.
* `seed_data.sql`: DML scripts to populate the database with sample testing data.
* `design_docs/`: Directory containing design artifacts:
    * `Conceptual_EER_Diagram.png`: The conceptual database model.
    * `Logical_Relational_Schema.png`: The normalized relational schema.
    * `Final_Implementation_Report.pdf`: Detailed documentation of the implementation and testing.


## 🧠 Database Design & Modeling

The system architecture followed a strict two-phase design process to ensure data integrity and normalization.

### 1. Conceptual Design (EER Diagram)
The initial model captures complex business rules, including recursive mentorships and disjoint specializations (Student/Faculty/Collaborator).

[Conceptual EER Diagram](design_docs/Conceptual_EER_Diagram.pdf)

### 2. Logical Design (Relational Schema)
The conceptual model was mapped to a relational schema normalized to 3NF. Foreign keys (arrows) indicate referential integrity constraints.

[Relational Schema](design_docs/Logical_Relational_Schema.pdf)

 ***3. Detailed Documentation:** For a full breakdown of the constraints, testing queries, and implementation challenges, please read the 
 
 [Final Implementation Report](design_docs/Final_Implementation_Report.pdf).


## ⚙️ Setup & Installation

**Prerequisites:** MySQL Server installed locally or remotely.

1. **Clone the repository**
   ```bash
   git clone https://github.com/shaury05/University_Laboratory_Database_Design.git
   cd University_Laboratory_Database_Design

```

2. **Set up the Database**
Open your MySQL client (Workbench or CLI) and run the SQL scripts in this order:
1. Execute `schema.sql` to build the tables and relationships.
2. Execute `seed_data.sql` to load sample data.


3. **Install Python Dependencies**
```bash
pip install mysql-connector-python

```


4. **Configure Connection**
Open `app.py` and update the `db_config` dictionary with your database credentials.
> **Note:** It is recommended to use environment variables for the password in a production environment.


5. **Run the Application**
```bash
python app.py

```
```
## 👥 Contributors

* **Shaury Pratap Singh** (Team Lead, Backend Logic)
* Abhiram Panuganti
* Rithvik Reddy

Developed for **CS 631: Data Management Systems Design** at NJIT.
