from kafka import KafkaConsumer
import json

job_desc_consumer = KafkaConsumer(
        "jd_topic",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset='earliest',  # Start reading from the earliest message
        group_id='jd_consumer_group',  # Assign a consumer group ID
        # value_deserializer=lambda x: json.loads(x).decode("utf-8")
    )

def process_job_description():
    """Consumes job descriptions from Kafka."""
    print("Consumer started. Waiting for messages...")
    print(type(job_desc_consumer))
    try:
        for message in job_desc_consumer:
            print("Message received:")
            job_data = message.value
            print("Job Description:", job_data.get('job_description'))
            return job_data.get('job_description')
            # Process the job description here (e.g., store in DB, perform analysis, etc.)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except KeyboardInterrupt:
        print("Consumer stopped.")
    except Exception as e:
        print("An error occurred:", e)


# Run the consumer
# process_job_description()
