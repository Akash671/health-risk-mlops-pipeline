import psycopg2

print("🔗 Connecting directly to Supabase Cloud Warehouse via pure Python sockets...")

new_patients_data = [
    {
        "Age": 30, "Gender": "Male", "BMI": 28.1, "Smoking Status": "Never", 
        "Alcohol Consumption (per week)": 2, "Physical Activity (hours/week)": 4.0, 
        "Sleep Duration (hours/day)": 9.5, "Chronic Disease History": "None", 
        "Stress Level (1-10)": 3, "Health Risk Level": "Low"
    },
    {
        "Age": 60, "Gender": "Female", "BMI": 35.4, "Smoking Status": "Current", 
        "Alcohol Consumption (per week)": 12, "Physical Activity (hours/week)": 1.0, 
        "Sleep Duration (hours/day)": 5.5, "Chronic Disease History": "Hypertension", 
        "Stress Level (1-10)": 8, "Health Risk Level": "High"
    }
]

try:
    conn = psycopg2.connect(
        host="aws-0-eu-west-1.pooler.supabase.com",
        port=5432,
        database="postgres",
        user="postgres.nevzmprqlpxjmgvbvkhh",
        password="Bug_killer@454545"
    )
    
    cursor = conn.cursor()
    
    for row in new_patients_data:
        insert_query = """
        INSERT INTO raw_patient_records 
        ("Age", "Gender", "BMI", "Smoking Status", "Alcohol Consumption (per week)", 
         "Physical Activity (hours/week)", "Sleep Duration (hours/day)", "Chronic Disease History", 
         "Stress Level (1-10)", "Health Risk Level") 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            row["Age"], row["Gender"], row["BMI"], row["Smoking Status"], 
            row["Alcohol Consumption (per week)"], row["Physical Activity (hours/week)"], 
            row["Sleep Duration (hours/day)"], row["Chronic Disease History"], 
            row["Stress Level (1-10)"], row["Health Risk Level"]
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("🚀 Success! New weekly data records successfully streamed and saved into Supabase!")

except Exception as e:
    print(f"❌ Connection Interrupted: {e}")
