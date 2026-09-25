from db import get_connection

try:
    connection = get_connection()
    print("SUCCESS: Connected to SkillSwap MySQL database!")
    connection.close()
except Exception as e:
    print("ERROR:", e)