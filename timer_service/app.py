from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from keycloak import KeycloakOpenID
from werkzeug.exceptions import HTTPException
from keycloak.exceptions import KeycloakGetError
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Time
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Настройки Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # Нужен для безопасной работы сессий


# Настройка базы данных
URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'
engine = create_engine(URL)
session_local = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks_nikulin'

    id = Column(Integer, primary_key=True)
    time = Column(Time, nullable=False)
    text = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            token = keycloak_openid.token(grant_type="password",
                                          username=username,
                                          password=password)
            session['token'] = token['access_token']
            if user_is_approved(session['token']):
                return redirect(url_for('index'))
            else:
                return "Access denied", 403
        except KeycloakGetError as e:
            return str(e), 400
    return render_template('login.html')

def user_is_approved(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return True
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.route('/save', methods=['POST'])
def save_task():
    time_now = datetime.datetime.now().time()
    text = request.form['text']

    session = session_local()
    new_task = Task(time=time_now, text=text)
    session.add(new_task)
    session.commit()
    session.close()

    return jsonify({'time': str(time_now), 'text': text})

@app.route('/')
def index():
    if 'token' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/tasks', methods=['GET'])
def get_tasks():
    session = session_local()
    try:
        tasks = session.query(Task).all()
        tasks_data = [{'time': str(task.time), 'text': task.text} for task in tasks]
        return jsonify(tasks_data)
    finally:
        session.close()

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
