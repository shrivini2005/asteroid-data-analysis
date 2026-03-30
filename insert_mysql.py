import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vinisha@2005",
    database="asteroid_db"
)

cursor = conn.cursor()

with open("C:\\Users\\user\\Downloads\\asteroids.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            # safe conversion
            def to_float(val):
                return float(val) if val not in ("", None) else 0

            def to_int(val):
                return int(val) if val not in ("", None) else 0

            # Insert into asteroids table
            cursor.execute("""
                INSERT INTO asteroids 
                (id, neo_reference_id, name, absolute_magnitude_h, diameter_min, diameter_max, hazardous)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                to_int(row["id"]),
                to_int(row["neo_reference_id"]),
                row["name"],
                to_float(row["absolute_magnitude_h"]),
                to_float(row["diameter_min"]),
                to_float(row["diameter_max"]),
                to_int(row["hazardous"])
            ))

            # Insert into close_approach table
            cursor.execute("""
                INSERT INTO close_approach 
                (id, close_approach_date, velocity, astronomical, miss_distance_km, miss_distance_lunar, orbiting_body)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                to_int(row["id"]),
                row["close_approach_date"],
                to_float(row["velocity"]),
                to_float(row["astronomical"]),
                to_float(row["miss_distance_km"]),
                to_float(row["miss_distance_lunar"]),
                row["orbiting_body"]
            ))

        except Exception as e:
            print("❌ Error row:", row)
            print("Reason:", e)

# ✅ commit MUST be here (outside loop)
conn.commit()

print("✅ Data inserted successfully!")

cursor.close()
conn.close()