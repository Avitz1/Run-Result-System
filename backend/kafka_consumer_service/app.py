import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend.run_result_service.source.models import RunResult

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://user:password@localhost/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()


def consume_kafka_events(topic, bootstrap_servers='localhost:29092'):
    from kafka import KafkaConsumer
    consumer = KafkaConsumer('run-results', bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')))

    with app.app_context():
        for message in consumer:
            data = message.value
            json_data = json.loads(data)
            run_result = RunResult.from_dict(json_data)
            db.session.add(run_result)
            db.session.commit()
            print(f"Message consumed and saved to DB: {data}")


if __name__ == '__main__':
    topic = 'run-results'
    db.init_app(app)
    consume_kafka_events(topic)
