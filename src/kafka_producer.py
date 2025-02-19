from kafka import KafkaProducer
import json

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    acks='all',
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_resume(resume_content, id):
    """Reads resume file and sends it to Kafka topic."""
    resume_data = {"id": id, "resume": resume_content}
    producer.send("resume_topic", resume_data)
    # producer.send('resume_topic', json.dumps(resume_data).encode('utf-8'))
    print(f"✅ Resume sent for {id}")

def send_job_description(job_desc):
    """Sends job description to Kafka topic."""
    print("inside send_job_description")
    job_data = {"job_description": job_desc}
    producer.send("jd_topic", job_data)
    producer.flush()
    print("✅ Job description sent!")