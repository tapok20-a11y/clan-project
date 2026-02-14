from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from db.database import init_db
from db.repository import get_accepted_forms, get_total_accepted

app = FastAPI(title="Анкеты Telegram-бота")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/accepted")
def accepted_forms_api():
    """API для общей системы/второго бота."""
    return {"total": get_total_accepted(), "items": get_accepted_forms()}


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    forms = get_accepted_forms()
    rows = "".join(
        f"<tr><td>{f['user_id']}</td><td>{f['username'] or '-'}</td><td>{f['full_name']}</td>"
        f"<td>{f['age']}</td><td>{f['hobby']}</td><td>{f['birth_date']}</td><td>{f['inviter']}</td><td>{f['created_at']}</td></tr>"
        for f in forms
    )
    return f"""
    <html>
    <head><meta charset='utf-8'><title>Анкеты</title></head>
    <body style='font-family: Arial; margin: 2rem;'>
        <h1>Принятые анкеты</h1>
        <p>Всего принятых: <b>{get_total_accepted()}</b></p>
        <table border='1' cellpadding='6' cellspacing='0'>
            <thead>
                <tr>
                    <th>User ID</th><th>Username</th><th>Имя</th><th>Возраст</th>
                    <th>О себе</th><th>Дата рождения</th><th>Пригласил</th><th>Создано</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </body>
    </html>
    """
