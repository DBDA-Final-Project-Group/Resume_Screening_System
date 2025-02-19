import threading
from kafka import KafkaConsumer
import json
from hdfs import InsecureClient

# To connect to WebHDFS by providing the IP of the HDFS host and the WebHDFS port.
client_hdfs = InsecureClient('http://localhost:9870', user='piyush')

resume_consumer = KafkaConsumer(
    "resume_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset='earliest',  # Start reading from the earliest message
    group_id='resume_consumer_group',  # Assign a consumer group ID
)

def process_resume():
    """Consumes resumes from Kafka and stores them in HDFS & Cassandra."""
    # while True:
    #     print("inside process_resume()")
    #     print(resume_consumer)
    #     for message in resume_consumer:
    #         print("inside loop")
    #         resume_data = message.value
    #         print(resume_data)
    #         resume_text = resume_data["resume"]
    #         id = resume_data["id"]
    #
    #         # Store resume in HDFS
    #         hdfs_path = f"/user/project/temp_resumes/{id}.txt"
    #         # hdfs.dump(resume_text, hdfs_path)
    #
    #         # To write a Dataframe to HDFS.
    #         with client_hdfs.write(hdfs_path, encoding='utf-8') as writer:
    #             writer.write(resume_text)
    #         print(f"✅ Resume stored in HDFS: {hdfs_path}")
    print("Consumer started. Waiting for messages...")
    print(resume_consumer)
    try:
        for message in resume_consumer:
            print("Message received:")
            resume_data = message.value
            print("Resume:", resume_data.get('resume'))
            resume_text = resume_data.get('resume')
            id = resume_data.get('id')

            print(resume_text)
            print(id)

            # Store resume in HDFS
            hdfs_path = f"/user/project/temp_resumes/{id}.txt"

            # To write a Dataframe to HDFS.
            with client_hdfs.write(hdfs_path, encoding='utf-8') as writer:
                writer.write(resume_text)
            print(f"✅ Resume stored in HDFS: {hdfs_path}")

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except KeyboardInterrupt:
        print("Consumer stopped.")
    except Exception as e:
        print("An error occurred:", e)

# process_resume()