from app import app, db

with app.app_context():
    db.drop_all()   # זה ימחק את כל הטבלאות הישנות
    db.create_all() # זה ייצור אותן מחדש עם העמודה של ה-AI
    print("בסיס הנתונים עודכן בהצלחה! ✅")
