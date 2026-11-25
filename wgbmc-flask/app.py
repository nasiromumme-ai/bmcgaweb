import os, secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from dotenv import load_dotenv
load_dotenv()
from pymysql.cursors import DictCursor
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key-before-deployment')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
CATEGORIES = {'Sadeen': 'Ida’ama Galii Sadeen', 'Idilee': 'Galii Idilee', 'MQopheessaa': 'Galii Mana Qopheessaa', 'Keessoo': 'Galii Keessoo'}

def db():
    return pymysql.connect(host=os.getenv('DB_HOST','localhost'), user=os.getenv('DB_USER','root'),
        password=os.getenv('DB_PASS',''), database=os.getenv('DB_NAME','galii_baha_oromiyaa'),
        charset='utf8mb4', cursorclass=DictCursor, autocommit=True)

def query(sql, args=(), one=False):
    conn=db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql,args)
            return cur.fetchone() if one else cur.fetchall()
    finally: conn.close()

def execute(sql,args=()):
    conn=db()
    try:
        with conn.cursor() as cur: cur.execute(sql,args)
    finally: conn.close()

def csrf_token():
    if 'csrf' not in session: session['csrf']=secrets.token_hex(32)
    return session['csrf']
@app.context_processor
def inject_globals(): return {'csrf_token':csrf_token,'is_admin':bool(session.get('admin_id')),'admin_username':session.get('admin_username','admin'),'categories':CATEGORIES}
@app.before_request
def check_csrf():
    if request.method=='POST':
        token=session.get('csrf','')
        if not token or not secrets.compare_digest(token,request.form.get('csrf','')):
            return 'CSRF validation failed.',403

def admin_required(fn):
    @wraps(fn)
    def wrapper(*a,**kw):
        if not session.get('admin_id'): return redirect(url_for('login'))
        return fn(*a,**kw)
    return wrapper

def compact_etb(n):
    n=float(n or 0)
    if abs(n)>=1e9:return f'{n/1e9:,.2f} B'
    if abs(n)>=1e6:return f'{n/1e6:,.2f} M'
    if abs(n)>=1e3:return f'{n/1e3:,.1f} K'
    return f'{n:,.2f}'

@app.route('/')
@app.route('/index')
def index():
    category=request.args.get('category','Sadeen'); category=category if category in CATEGORIES else 'Sadeen'
    entity=request.args.get('entity','').strip(); search=request.args.get('q','').strip(); perf=request.args.get('perf','ALL')
    sql='SELECT * FROM revenue_records WHERE category=%s'; params=[category]
    if entity: sql+=' AND entity_name=%s'; params.append(entity)
    if search: sql+=' AND entity_name LIKE %s'; params.append('%'+search+'%')
    if perf=='HIGH': sql+=' AND is_summary=0 AND annual_percent>=45'
    elif perf=='MID': sql+=' AND is_summary=0 AND annual_percent>=35 AND annual_percent<45'
    elif perf=='LOW': sql+=' AND is_summary=0 AND annual_percent<35'
    sql+=' ORDER BY is_summary ASC, serial_no ASC, entity_name ASC'
    rows=query(sql,params); entities=[r['entity_name'] for r in query('SELECT DISTINCT entity_name FROM revenue_records WHERE category=%s AND is_summary=0 ORDER BY entity_name',(category,))]
    detail=[r for r in rows if not int(r['is_summary'])]; summaries=[r for r in rows if int(r['is_summary'])]
    kpi=summaries[0] if not entity and not search and perf=='ALL' and summaries else None
    if kpi:
        annual_plan=float(kpi['annual_plan']); annual_actual=float(kpi['annual_actual']); daily_plan=float(kpi['daily_plan']); daily_actual=float(kpi['daily_actual']); annual_pct=float(kpi['annual_percent']); daily_pct=float(kpi['daily_percent'])
    else:
        annual_plan=sum(float(r['annual_plan']) for r in detail); annual_actual=sum(float(r['annual_actual']) for r in detail)
        daily_plan=sum(float(r['daily_plan']) for r in detail); daily_actual=sum(float(r['daily_actual']) for r in detail)
        annual_pct=annual_actual/annual_plan*100 if annual_plan else 0; daily_pct=daily_actual/daily_plan*100 if daily_plan else 0
    chart_rows=sorted(detail,key=lambda r:float(r['annual_actual']),reverse=True); top=chart_rows[:10]
    pct_rows=[r for r in chart_rows if float(r['annual_percent'])>0][:10]
    chart={'labels':[r['entity_name'] for r in top], 'plan':[float(r['annual_plan'])/1e6 for r in top], 'actual':[float(r['annual_actual'])/1e6 for r in top], 'pctLabels':[r['entity_name'] for r in pct_rows], 'pctValues':[float(r['annual_percent']) for r in pct_rows]}
    mix={}
    for c in ['Idilee','Keessoo','MQopheessaa']:
        r=query('SELECT annual_actual FROM revenue_records WHERE category=%s AND is_summary=1 ORDER BY id LIMIT 1',(c,),one=True); mix[c]=float(r['annual_actual']) if r else 0
    if entity:
        for c in mix:
            r=query('SELECT annual_actual FROM revenue_records WHERE category=%s AND entity_name=%s AND is_summary=0 LIMIT 1',(c,entity),one=True); mix[c]=float(r['annual_actual']) if r else 0
    return render_template('index.html',category=category,entity=entity,search=search,perf=perf,rows=rows,detail_rows=detail,entities=entities,
        annual_plan=annual_plan,annual_actual=annual_actual,daily_plan=daily_plan,daily_actual=daily_actual,annual_pct=annual_pct,daily_pct=daily_pct,
        chart=chart,mix=mix,compact_etb=compact_etb)

@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('admin_id'): return redirect(url_for('admin'))
    if request.method=='POST':
        user=request.form.get('username','').strip(); password=request.form.get('password','')
        row=query('SELECT id,username,password_hash FROM admins WHERE username=%s LIMIT 1',(user,),one=True)
        if row and check_password_hash(row['password_hash'],password):
            session.clear(); session['admin_id']=row['id']; session['admin_username']=row['username']; csrf_token(); return redirect(url_for('admin'))
        flash('Username ykn password sirrii miti.','error')
    return render_template('login.html')

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin():
    category=request.args.get('category','Sadeen'); category=category if category in CATEGORIES else 'Sadeen'
    edit=None
    if request.args.get('edit','').isdigit(): edit=query('SELECT * FROM revenue_records WHERE id=%s AND is_summary=0',(int(request.args['edit']),),one=True)
    records=query('SELECT * FROM revenue_records WHERE category=%s AND is_summary=0 ORDER BY serial_no,entity_name',(category,))
    return render_template('admin.html',category=category,edit=edit,records=records)

@app.route('/save',methods=['POST'])
@admin_required
def save():
    category=request.form.get('category',''); name=request.form.get('entity_name','').strip()
    if category not in CATEGORIES: return 'Gosa galii sirrii miti.',400
    if not name: return 'Maqaan barbaachisa.',400
    try:
        plan=max(0,float(request.form.get('annual_plan') or 0)); actual=max(0,float(request.form.get('annual_actual') or 0)); dplan=max(0,float(request.form.get('daily_plan') or 0)); dactual=max(0,float(request.form.get('daily_actual') or 0))
        serial=int(request.form['serial_no']) if request.form.get('serial_no') else None
    except ValueError: return 'Lakkoofsi galfame sirrii miti.',400
    vals=(category,serial,name,plan,actual,round(actual/plan*100,2) if plan else 0,dplan,dactual,round(dactual/dplan*100,2) if dplan else 0)
    rid=request.form.get('id','')
    if rid.isdigit() and int(rid):
        execute('UPDATE revenue_records SET category=%s,serial_no=%s,entity_name=%s,annual_plan=%s,annual_actual=%s,annual_percent=%s,daily_plan=%s,daily_actual=%s,daily_percent=%s WHERE id=%s AND is_summary=0',vals+(int(rid),))
    else:
        execute('INSERT INTO revenue_records(category,serial_no,entity_name,annual_plan,annual_actual,annual_percent,daily_plan,daily_actual,daily_percent,is_summary) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,0)',vals)
    return redirect(url_for('admin',category=category,saved=1))

@app.route('/delete',methods=['POST'])
@admin_required
def delete():
    rid=request.form.get('id',''); category=request.form.get('category','Sadeen')
    if rid.isdigit(): execute('DELETE FROM revenue_records WHERE id=%s AND is_summary=0',(int(rid),))
    return redirect(url_for('admin',category=category))

@app.route('/change-password',methods=['POST'])
@admin_required
def change_password():
    current=request.form.get('current_password',''); new=request.form.get('new_password','')
    if len(new)<10: flash('Password yoo xiqqaate 10 characters ta’uu qaba.','error'); return redirect(url_for('admin'))
    row=query('SELECT password_hash FROM admins WHERE id=%s',(session['admin_id'],),one=True)
    if not row or not check_password_hash(row['password_hash'],current): flash('Password ammaa sirrii miti.','error'); return redirect(url_for('admin'))
    execute('UPDATE admins SET password_hash=%s WHERE id=%s',(generate_password_hash(new),session['admin_id']))
    flash('Password milkaa’inaan jijjiirame.','success'); return redirect(url_for('admin'))

if __name__=='__main__': app.run(host='127.0.0.1',port=int(os.getenv('PORT',5000)),debug=os.getenv('FLASK_DEBUG')=='1')
