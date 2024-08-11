from datetime import datetime
from flask_mysqldb import MySQL

db = MySQL

class Reservation:
    def __init__(self, id, date, doctor, details):
        self.id = id
        self.date = date
        self.doctor = doctor
        self.details = details
    
    @classmethod
    def get_all(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = "select r.id, r.date, r.details, d.name from reservations r LEFT JOIN doctors d ON r.doctor = d.id order by r.date ASC;"
            cursor.execute(sql)
            rows = cursor.fetchall()
            reservations = []
            for row in rows:
                if len(row) >= 4:  
                    reservation = {
                        "id": row[0],
                        "date": row[1],
                        "doctor": row[2],
                        "details": row[3]
                    }
                    if isinstance(reservations, list):
                        reservations.append(reservation)
                    else:
                        raise Exception("reservations is not a list.")
                else:
                    raise Exception("Unexpected number of columns in row.")
            return reservations
        except Exception as ex:
            raise Exception(f"Error fetching reservations: {str(ex)}")
