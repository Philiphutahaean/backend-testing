from flask import Flask, request
import pymysql  # Replace with your database library

# Cloud SQL connection details (replace with your own)
HOST = "your_cloud_sql_instance_connection_string"  # Replace with GCP credentials
USER = "your_username"
PASSWORD = "your_password"
DATABASE = "your_database_name"

app = Flask(__name__)

@app.route("/sensor_data", methods=["POST"])
def receive_sensor_data():
  # Get data from request
  data = request.get_json()

  # Parse sensor data
  nutrient_values = data.get("nutrient_values")
  if not nutrient_values:
    return "Missing nutrient_values data in request.", 400

  # Convert nutrient values to list
  nutrient_values = [float(value) for value in nutrient_values.split(",")]

  # Predict plant recommendation using KNN classifier
  predicted_plant = knn.predict([nutrient_values])[0]

  # Connect to Cloud SQL database
  connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
  cursor = connection.cursor()

  # Prepare SQL statement (modify for your table structure)
  sql = "INSERT INTO sensor_data (N, P, K, humidity, pH, temperature, recommended_plant) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  cursor.execute(sql, nutrient_values + [predicted_plant])

  # Save changes and close connection
  connection.commit()
  connection.close()

  return f"Recommended plant: {predicted_plant}", 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3000)  # Listen on all interfaces and port 80