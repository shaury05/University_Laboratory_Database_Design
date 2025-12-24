# Research Lab Management System

A comprehensive database application designed to streamline the administrative operations of a university research laboratory. This system manages the complex relationships between lab members, grant funding, research projects, equipment usage, and academic publications.

The project demonstrates a full-lifecycle database implementation: from **EER Conceptual Modeling** to **Relational Schema Normalization** and a **Python-based CLI application** layer.

## 🚀 Key Features

* 
**Member Management:** Tracks a hierarchy of lab members including Faculty, Students (PhD/Masters), and External Collaborators using supertype/subtype relationships.


* 
**Grant & Project Tracking:** Manages funding sources and their allocation to specific research projects and personnel.


* 
**Equipment Concurrency Control:** Implements **Application-Level Validation** to enforce business rules that standard SQL constraints cannot handle (e.g., preventing equipment checkout if active users ≥ 3).


* 
**Recursive Relationships:** Handles internal mentorship programs where lab members mentor other members.


* **Analytical Reporting:** Generates insights such as:
* Average student publications per major.


* Active projects filtered by grant and date ranges.


* Top publishing members.





## 🛠️ Tech Stack

* 
**Database:** MySQL 9.5 


* 
**Language:** Python 3.x 


* 
**Driver:** `mysql-connector-python` 


* **Design Tools:** EER Modeling, Relational Algebra

## 📂 Repository Structure

* `app.py`: The main Python entry point containing the CLI menu and application logic.
* `schema.sql`: DDL scripts to create the database, tables, views, and constraints.
* `seed_data.sql`: DML scripts to populate the database with sample testing data.
* `ER_Diagram.png`: Visual representation of the Enhanced Entity-Relationship model.

## ⚙️ Setup & Installation

**Prerequisites:** MySQL Server installed locally or remotely.

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Research-Lab-Management-System.git
cd Research-Lab-Management-System

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



## 🧠 Database Design Highlights

This project addresses several complex data modeling challenges:

* **Normalization:** The schema is normalized to 3NF to reduce redundancy, particularly in the handling of publication authorships and project funding.
* **Complex Constraints:**
* 
*Recursive Logic:* The `LAB_MEMBER` table includes a foreign key `MENTOR` referencing itself to create a hierarchy.


* 
*Transaction Safety:* Python logic wraps SQL transactions to ensure equipment status is only updated to 'In Use' after validating current usage counts.




* 
**Advanced Querying:** Utilizes `LEFT JOIN` operations to ensure accurate reporting (e.g., including majors with zero publications in statistical averages).



## 👥 Contributors

* 
**Shaury Pratap Singh** (Team Lead, Backend Logic) 


* Abhiram Panuganti 


* Rithvik Reddy 



Developed for **CS 631: Data Management Systems Design** at NJIT.
