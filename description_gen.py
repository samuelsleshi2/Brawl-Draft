import sqlite3
from google import genai
import os
import time
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("NO API KEY FOUND")
    exit()

print(f"USING KEY ENDING IN: ...{api_key[-4:]}")

client = genai.Client(api_key=api_key)
conn = sqlite3.connect("draft.db")
cursor = conn.cursor()

cursor.execute("UPDATE rankings SET description = 'Mobile assassin; jumps over attacks.' WHERE brawler_name LIKE '%Mico%'")
conn.commit()

cursor.execute("SELECT id, mode, map_name, brawler_name, pick FROM rankings WHERE description IS NULL")
rows = cursor.fetchall()

print(f"PROCESSING {len(rows)} ROWS")
time.sleep(2) 

for index, row in enumerate(rows):
    row_id, mode, map_name, brawler_name, pick = row
    
    success = False
    
    while not success:
        try:
            print(f"[{index+1}/{len(rows)}] Generating for {brawler_name}...")
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite", 
                contents=f"Explain in 10 words why {brawler_name} is a strong {pick} pick for {map_name} in {mode}."
            )
            
            cursor.execute("UPDATE rankings SET description = ? WHERE id = ?", (response.text, row_id))
            conn.commit()
            print("SAVED")
            success = True
            
            time.sleep(10)
            
        except Exception as e:
            if "429" in str(e):
                print("RATE LIMIT HIT. WAITING 60s...")
                time.sleep(60)
            else:
                print(f"ERROR: {e}")
                time.sleep(5)

conn.close()