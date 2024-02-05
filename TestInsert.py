# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 06:53:29 2024

@author: Pongo
"""

from pymongo import MongoClient

# Replace this with your MongoDB connection string
mongo_uri = 'mongodb+srv://rafyeffendy772:65798834@jumpheightrecord.tlt343i.mongodb.net/'

# Replace with your MongoDB database and collection names
database_name = 'test'
collection_name_users = 'Users'

# Replace with your Ultrasonic data
ultrasonic_visual_data = '69'
ultrasonic_sensor_data = '420'
username = 'user1'

def insert_ultrasonic_data(username, visual_data, sensor_data):
    client = MongoClient(mongo_uri)
    db = client[database_name]

    # Check if the user exists
    user_data = db[collection_name_users].find_one({'username': username})
    if user_data:
        # Insert Ultrasonic data into the user's collection
        user_collection_name = user_data['collection_name']
        user_collection = db[user_collection_name]
        user_collection.insert_one({
            'UltrasonicVisualData': visual_data,
            'UltrasonicSensorData': sensor_data
        })
        print(f"Ultrasonic data inserted for user '{username}'")
    else:
        print(f"User '{username}' not found")

if __name__ == '__main__':
    insert_ultrasonic_data(username, ultrasonic_visual_data, ultrasonic_sensor_data)

