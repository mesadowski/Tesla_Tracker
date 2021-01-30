#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 19:08:43 2021
@author: michaelsadowski
"""
import myTesla
import os
import boto3
from datetime import datetime
import uuid


EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']

def lambda_handler(event,context):
    
    my_car = myTesla.connect(EMAIL, PASSWORD)
    charge_state = my_car.charge_state()
    vehicle_state = my_car.vehicle_state()
    climate_state = my_car.climate_state()
    drive_state = my_car.drive_state()
    
    if ('error' in vehicle_state):
        print (vehicle_state['error'])
    else:
        battery_level = charge_state['response']['usable_battery_level']
        lat = drive_state['response']['latitude']
        long = drive_state['response']['longitude']
        heading = drive_state['response']['heading']
        speed = drive_state['response']['speed']
        power = drive_state['response']['power']
        locked = vehicle_state['response']['locked']
        odometer = vehicle_state['response']['odometer']
        climate_on = climate_state['response']['is_climate_on']
        inside_temp = climate_state['response']['inside_temp']
        outside_temp = climate_state['response']['outside_temp']

        recordID = str(uuid.uuid4()) #generate a unique record ID
        dt = datetime.now()

        #Create record in DynamoDB table
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
        table.put_item(
            Item={
                'Record_ID' : recordID,
                'DateTime' : str(dt),
                'battery_level' : battery_level,
                'lat' : str(lat),
                'long' : str(long),
                'heading' : str(heading),
                'speed' : str(speed),
                'power' : power,
                'locked' : locked,
                'odometer' : str(odometer),
                'climate_on' : climate_on,
                'inside_temp' : str(inside_temp),
                'outside_temp' : str(outside_temp)
                }
            )
        