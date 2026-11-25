# Chiro Revenue Reporting — Python Flask

PHP projectichi Python Flask irratti jijjiirame. Dashboard, filters/search, KPI, Chart.js charts, admin login, galmee CRUD, CSRF protection fi password jijjiiruun ni jira. CSS fi MySQL schema/data jalqabaa waliin qabateera.

## 1. Python environment

Python 3.10+ fi MySQL/MariaDB barbaachisa.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configuration

`.env.example` gara `.env` copy godhi; DB_HOST, DB_NAME, DB_USER, DB_PASS sirreessi. `SECRET_KEY` immoo dheerataa fi iccitii ta’e kaa’i.

```bash
# Windows PowerShell
Copy-Item .env.example .env
# Linux/macOS
cp .env.example .env
```

`app.py` keessatti `.env` ofumaan akka fe’uuf sarara jalqabaa irratti `from dotenv import load_dotenv; load_dotenv()` dabali; ykn environment variables OS keessatti qindeessi.

## 3. Database fi odeeffannoo duraanii

Database duwwaa uumi, itti aansuun SQL dump jalqabaa import godhi:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS galii_baha_oromiyaa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p galii_baha_oromiyaa < chirorevenue.sql
python init_db.py
```

Yoo DB username/password adda ta’e command sana keessatti sirreessi. `chirorevenue.sql` dump jalqabaa irraa tables fi rows jiran hunda galcha. `init_db.py` tables hin jirre qofa uuma, achiis admin password Python waliin walsimsiisa; data galii hin haqamu. Yoo data jalqabaa hin barbaadne, `python init_db.py` qofti database/tables duwwaa uuma.

**Admin jalqabaa:** username `admin`, password `ChangeMe123!`. Yeroo jalqaba seentu password kana battalumatti jijjiiri.

## 4. App jalqabi

```bash
python app.py
```

Browser:
- Dashboard: http://127.0.0.1:5000/
- Admin: http://127.0.0.1:5000/login

## Faayilota

- `app.py` — Flask routes, MySQL queries, sessions, CRUD, calculations
- `templates/` — dashboard, login, admin HTML/Jinja templates
- `static/style.css` — CSS PHP projectii irraa eegame
- `chirorevenue.sql` — database fi odeeffannoo jalqabaa
- `init_db.py` — database/tables uumuu fi admin jalqabaa qopheessuu

Chart.js CDN fayyadama; chart agarsiisuuf internet browser keessatti barbaachisa. Production irratti `SECRET_KEY` cimaa, HTTPS, DB credentials nageenya qabu, backup fi `debug` dhaamsuu mirkaneessi.
