import mysql.connector
import sys


db_config = {
    'user': 'root',
    'password': 'my_password',  #put your password here
    'host': 'localhost',
    'database': 'ResearchLabManager'
}

def get_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

def execute_query(sql, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        if fetch:
            result = cur.fetchall()
            return result
        else:
            conn.commit()
            print(">> Action Successful.")
    except mysql.connector.Error as err:
        print(f">> Error: {err}")
    finally:
        conn.close()

# ==========================================
# MAIN MENU 
# ==========================================
def main_menu():
    while True:
        print("\n" + "="*60)
        print("      RESEARCH LAB MANAGER SYSTEM")
        print("="*60)
   
        print("1. PROJECT AND MEMBER MANAGEMENT")
        print("2. EQUIPMENT USAGE TRACKING")
        print("3. GRANT AND PUBLICATION REPORTING")
        print("4. Exit")
        
        choice = input("\nEnter Selection: ")
        
        if choice == '1': menu_one_management()
        elif choice == '2': menu_two_equipment()
        elif choice == '3': menu_three_reporting()
        elif choice == '4': break

# ==========================================
# 1. PROJECT AND MEMBER MANAGEMENT
# ==========================================
def menu_one_management():
    while True:
        print("\n--- [1] PROJECT & MEMBER MANAGEMENT ---")
        print("MEMBERS:")
        print("  1. List Members")
        print("  2. Add Member")
        print("  3. Update Member Name")
        print("  4. Remove Member")
        print("PROJECTS:")
        print("  5. List Projects (Display Status)")
        print("  6. Add Project")
        print("  7. Update Project Title")
        print("  8. Remove Project")
        print("QUERIES:")
        print("  9. Show Members funded by a Grant")
        print("  10. Show Mentorships in a Project")
        print("  0. Back to Main Menu")
        
        sel = input("Select: ")

        # --- MEMBER CRUD ---
        if sel == '1':
            rows = execute_query("SELECT * FROM LAB_MEMBER", fetch=True)
            for r in rows: print(r)
        
        elif sel == '2':
            mid = input("ID: ")
            name = input("Name: ")
            mtype = input("Type (Faculty/Student/Collaborator): ")
            execute_query("INSERT INTO LAB_MEMBER (MID, NAME, JOINDATE, MTYPE) VALUES (%s, %s, CURDATE(), %s)", (mid, name, mtype))

        elif sel == '3':
            mid = input("Member ID to Update: ")
            name = input("New Name: ")
            execute_query("UPDATE LAB_MEMBER SET NAME=%s WHERE MID=%s", (name, mid))

        elif sel == '4':
            mid = input("Member ID to Delete: ")
            execute_query("DELETE FROM LAB_MEMBER WHERE MID=%s", (mid,))

        # --- PROJECT CRUD ---
        elif sel == '5':
            # "Display the status of a project"
            rows = execute_query("SELECT PID, TITLE, SDATE, EDATE FROM PROJECT", fetch=True)
            for r in rows: 
                status = "Active" if r[3] is None else "Completed"
                print(f"ID: {r[0]} | Title: {r[1]} | Status: {status}")

        elif sel == '6':
            pid = input("ID: ")
            title = input("Title: ")
            leader = input("Leader ID (Faculty): ")
            execute_query("INSERT INTO PROJECT (PID, TITLE, SDATE, LEADER) VALUES (%s, %s, CURDATE(), %s)", (pid, title, leader))

        elif sel == '7':
            pid = input("Project ID: ")
            title = input("New Title: ")
            execute_query("UPDATE PROJECT SET TITLE=%s WHERE PID=%s", (title, pid))

        elif sel == '8':
            pid = input("Project ID to Delete: ")
            execute_query("DELETE FROM PROJECT WHERE PID=%s", (pid,))

        # --- SPECIFIC QUERIES ---
        elif sel == '9':
            gid = input("Enter Grant ID: ")
            rows = execute_query("""SELECT DISTINCT M.NAME FROM LAB_MEMBER M 
                                    JOIN WORKS W ON M.MID=W.MID 
                                    JOIN FUNDS F ON W.PID=F.PID WHERE F.GID=%s""", (gid,), fetch=True)
            for r in rows: print(f"- {r[0]}")

        elif sel == '10':
            pid = input("Enter Project ID: ")
            rows = execute_query("""SELECT Mentee.NAME, Mentor.NAME FROM LAB_MEMBER Mentee 
                                    JOIN LAB_MEMBER Mentor ON Mentee.MENTOR=Mentor.MID
                                    JOIN WORKS W1 ON Mentee.MID=W1.MID
                                    JOIN WORKS W2 ON Mentor.MID=W2.MID
                                    WHERE W1.PID=%s AND W2.PID=%s""", (pid, pid), fetch=True)
            for r in rows: print(f"Mentee: {r[0]} | Mentor: {r[1]}")

        elif sel == '0': break

# ==========================================
# 2. EQUIPMENT USAGE TRACKING
# ==========================================
def menu_two_equipment():
    while True:
        print("\n--- [2] EQUIPMENT USAGE TRACKING ---")
        print("1. List Equipment (Show Status)")
        print("2. Add Equipment")
        print("3. Remove Equipment")
        print("4. Checkout Equipment")
        print("5. Return Equipment")
        print("6. Show Current Users of Equipment")
        print("0. Back to Main Menu")
        sel = input("Select: ")

        if sel == '1':
            rows = execute_query("SELECT EID, ENAME, STATUS FROM EQUIPMENT", fetch=True)
            for r in rows: print(f"{r[0]}: {r[1]} [{r[2]}]")

        elif sel == '2':
            eid = input("ID: ")
            name = input("Name: ")
            etype = input("Type: ")
            execute_query("INSERT INTO EQUIPMENT (EID, ETYPE, ENAME, STATUS, PDATE) VALUES (%s, %s, %s, 'Available', CURDATE())", (eid, etype, name))

        elif sel == '3':
            eid = input("Equipment ID to Remove: ")
            execute_query("DELETE FROM EQUIPMENT WHERE EID=%s", (eid,))

        elif sel == '4':
            eid = input("Equipment ID: ")
            mid = input("Member ID: ")
            # CONSTRAINT CHECK
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM USES WHERE EID=%s AND EDATE IS NULL", (eid,))
            count = cur.fetchone()[0]
            conn.close()

            if count >= 3:
                print(">> ERROR: Max 3 users limit reached!")
            else:
                execute_query("INSERT INTO USES (MID, EID, SDATE) VALUES (%s, %s, CURDATE())", (mid, eid))
                execute_query("UPDATE EQUIPMENT SET STATUS='In Use' WHERE EID=%s", (eid,))

        elif sel == '5':
            eid = input("Equipment ID: ")
            mid = input("Member ID: ")
            execute_query("UPDATE USES SET EDATE=CURDATE() WHERE EID=%s AND MID=%s AND EDATE IS NULL", (eid, mid))
            execute_query("UPDATE EQUIPMENT SET STATUS='Available' WHERE EID=%s", (eid,))

        elif sel == '6':
            eid = input("Equipment ID: ")
            rows = execute_query("""SELECT M.NAME, P.TITLE FROM LAB_MEMBER M 
                                    JOIN USES U ON M.MID=U.MID 
                                    JOIN WORKS W ON M.MID=W.MID 
                                    JOIN PROJECT P ON W.PID=P.PID
                                    WHERE U.EID=%s AND U.EDATE IS NULL""", (eid,), fetch=True)
            for r in rows: print(f"User: {r[0]} | Project: {r[1]}")

        elif sel == '0': break

# ==========================================
# 3. GRANT AND PUBLICATION REPORTING
# ==========================================
def menu_three_reporting():
    while True:
        print("\n--- [3] GRANT AND PUBLICATION REPORTING ---")
        print("1. Member with Highest Publications")
        print("2. Avg Student Pubs per Major")
        print("3. Count Active Projects by Grant & Date")
        print("4. Top 3 Members on Grant (Most Pubs)")
        print("0. Back to Main Menu")
        sel = input("Select: ")

        if sel == '1':
            rows = execute_query("""SELECT M.NAME, COUNT(*) as C FROM LAB_MEMBER M 
                                    JOIN PUBLISHES P ON M.MID=P.MID GROUP BY M.MID ORDER BY C DESC LIMIT 1""", fetch=True)
            if rows: print(f"Top Publisher: {rows[0][0]} ({rows[0][1]} pubs)")

        elif sel == '2':
            rows = execute_query("""SELECT S.MAJOR, COUNT(P.PID)/COUNT(DISTINCT S.MID) FROM STUDENT S 
                                    LEFT JOIN PUBLISHES P ON S.MID=P.MID GROUP BY S.MAJOR""", fetch=True)
            for r in rows: print(f"{r[0]}: {float(r[1]):.2f}")

        elif sel == '3':
            gid = input("Grant ID: ")
            d = input("Date (YYYY-MM-DD): ")
            rows = execute_query("""SELECT COUNT(*) FROM PROJECT P 
                                    JOIN FUNDS F ON P.PID=F.PID 
                                    WHERE F.GID=%s AND (P.SDATE <= %s AND (P.EDATE >= %s OR P.EDATE IS NULL))""", (gid, d, d), fetch=True)
            print(f"Active Projects: {rows[0][0]}")

        elif sel == '4':
            gid = input("Grant ID: ")
            rows = execute_query("""SELECT M.NAME, COUNT(Pub.PID) as C 
                                    FROM LAB_MEMBER M 
                                    JOIN WORKS W ON M.MID=W.MID 
                                    JOIN FUNDS F ON W.PID=F.PID
                                    LEFT JOIN PUBLISHES Pub ON M.MID=Pub.MID
                                    WHERE F.GID=%s
                                    GROUP BY M.MID ORDER BY C DESC LIMIT 3""", (gid,), fetch=True)
            for r in rows: print(f"- {r[0]} ({r[1]} pubs)")

        elif sel == '0': break

if __name__ == "__main__":
    main_menu()