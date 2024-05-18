from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Time
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime

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

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def service_alive():
    return jsonify({'message': 'service alive'}), 200

@app.route('/', methods=['GET'])
def index():
    session = session_local()
    tasks = session.query(Task).all()
    session.close()
    return render_template('index.html', tasks=tasks)


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
