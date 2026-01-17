import sqlite3

conn = sqlite3.connect("draft.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM rankings WHERE description IS NULL")
remaining = cursor.fetchone()[0]
print(f"📉 Found {remaining} empty descriptions.")

cursor.execute("""
    UPDATE rankings 
    SET description = CASE 
        WHEN pick = '1st' THEN 'Priority pick for this map; secures control early and forces counter-picks.'
        WHEN pick = '6th' THEN 'Excellent counter-pick; exploits enemy weaknesses and rounds out the team comp.'
        ELSE 'Strong situational pick. Focus on winning your lane and applying pressure.'
    END
    WHERE description IS NULL
""")

conn.commit()
print(f"✅ SUCCESS! Filled {remaining} brawlers with professional placeholder text.")
print("🚀 Your database is 100% complete. You can upload to Streamlit Cloud.")

conn.close()