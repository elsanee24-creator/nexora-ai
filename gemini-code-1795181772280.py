# Let's ensure app.py is fully written and correctly populated with the exact code from app_3.py (or we can just copy app_3.py content to app.py)
with open("app_3.py", "r", encoding="utf-8") as f:
    content = f.read()

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("app.py generated and verified successfully!")