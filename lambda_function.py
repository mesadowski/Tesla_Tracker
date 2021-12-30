#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
#import sqlite3
from datetime import datetime
import boto3
import uuid
import os

import teslapy

EMAIL = os.environ['EMAIL']

def parameter_store_load():   # Get the tokens and other params from AWS Parameter Store
    ssm_client = boto3.client('ssm', region_name='us-east-1')    
    param = ssm_client.get_parameter(
            Name='My_Tesla_Parameters',
            WithDecryption=True
            )
    cache = param['Parameter']['Value']
    cache_json = json.loads(cache)
    return cache_json

def parameter_store_save(cache):    # Save the tokens and other params in AWS Parameter Store
    ssm_client = boto3.client('ssm', region_name='us-east-1')
    str_json = json.dumps(cache)
    response = ssm_client.put_parameter(
        Name='My_Tesla_Parameters',
        Value = str_json,
        Type='SecureString',
        Overwrite=True   
        )
    return
    
def main():
    
    try:   
        tesla = teslapy.Tesla(EMAIL, cache_loader=parameter_store_load, cache_dumper=parameter_store_save)
        
        vehicles = tesla.vehicle_list()
        #vehicles[0].sync_wake_up()   # Wake up the car. Comment out to avoid battery drain
        print(vehicles[0])
        
        cardata = vehicles[0].get_vehicle_data()
          
        battery_level = cardata['charge_state']['usable_battery_level']
        charge_added = cardata['charge_state']['charge_energy_added']
        lat = cardata['drive_state']['latitude']
        long = cardata['drive_state']['longitude']
        heading = cardata['drive_state']['heading']
        speed = cardata['drive_state']['speed']
        power = cardata['drive_state']['power']
        locked = cardata['vehicle_state']['locked']
        odometer = cardata['vehicle_state']['odometer']
        climate_on = cardata['climate_state']['is_climate_on']
        inside_temp = cardata['climate_state']['inside_temp']
        outside_temp = cardata['climate_state']['outside_temp']
        
        recordID = str(uuid.uuid4()) #generate a unique record ID
        dt = datetime.now()
        
        #Create record in the DynamoDB table
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table(os.environ['DB_TABLE_NAME'])  # Get the table name from the Lamda environment
        table.put_item(Item=
                {
                'Record_ID' : recordID,
                'DateTime' : str(dt),
                'battery_level' : battery_level,
                'charge_added' : str(charge_added),
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
                })
        
        print(battery_level)  # print something for debug purposes
        
    except teslapy.HTTPError as e:
        print(e)
        
    return

def lambda_handler(event,context):    
    main()
