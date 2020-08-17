from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import os
import json
import boto3 
import botocore
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
#access_key = os.environ['AWS_ACCESS_KEY_ID']
#secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
#service_point = os.environ['service_point']
access_key = "UBGGDNRHCQLXDF0741O8"
service_point = "http://ceph-route-rook-ceph.apps.jweng-ocp.shiftstack.com"
secret_key = "OkNuZihfaNgNcPgirlr5GTz9xXXHlUkZHDGUvhMN"


s3client = boto3.client('s3', endpoint_url=service_point,
                       aws_access_key_id = access_key,
                       aws_secret_access_key = secret_key,
                        use_ssl = True if 'https' in service_point else False)
app = Flask(__name__)


@app.route('/', methods=['POST'])
def classify():
    print("IN CLASSIFY++++++++++++++++")
    # S3 object location 
    image_location = {} 

    # Parse the given json 
    data = request.get_json()
    logging.info(data)
    image_location['object_name'] = data['s3']['object']['key']
    image_location['bucket_name'] =  data['s3']['bucket']['name'] 
    image_path = '/tmp/' + image_location['object_name']
    
    # Fetch the wanted s3 object 
    s3client.download_file(image_location['bucket_name'], image_location['object_name'], image_path)

    # Run image classification algorithm
    #result = run_inference_on_image(image_path) 
    print("notifcation: " + str(image_path))
    # Return analysis
    logging.info(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
