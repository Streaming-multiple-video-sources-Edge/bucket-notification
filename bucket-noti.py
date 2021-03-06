'''
@Author Shon Paz
@Date   16/02/2020
'''

import boto3
import json
import botocore
import argparse

'''This class configures bucket notifications for both kafka and rabbitmq endpoints for real-time message queuing'''


class Notifier:
		
    def __init__(self):

        # creates all needed arguments for the program to run
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--endpoint-url', help="endpoint url for s3 object storage", required=True)
        parser.add_argument('-a', '--access-key', help='access key for s3 object storage', required=True)
        parser.add_argument('-s', '--secret-key', help='secret key for s3 object storage', required=True)
        parser.add_argument('-b', '--bucket-name', help='s3 bucket name', required=True)
        #parser.add_argument('-ke', '--kafka-endpoint', help='kafka endpoint in which rgw will send notifications to', required=False)
        #parser.add_argument('-ae', '--amqp-endpoint', help='amqp endpoint in which rgw will send notifications to', required=False)
        parser.add_argument('-he', '--http-endpoint', help='http endpoint in which rgw will send notifications to', required=False)
        parser.add_argument('-t', '--topic', help='topic name in which rgw will send notifications to', required=True)
        parser.add_argument('-f', '--filter', help='filter such as prefix, suffix, metadata or tags', required=False)
        #parser.add_argument('-o', '--opaque', help='opaque data that will be sent in the notifications', required=False)
        #parser.add_argument('-x', '--exchange', help='amqp exchange name (mandatory for amqp endpoints)', required=False)
        parser.add_argument('-n', '--notification', help='notification name, allows for setting multiple notifications on the same bucket', required=False, default="configuration")
				
        # parsing all arguments
        args = parser.parse_args()
				
        # building instance vars
        self.endpoint_url = args.endpoint_url
        self.access_key = args.access_key
        self.secret_key = args.secret_key
        self.bucket_name = args.bucket_name
        #self.kafka_endpoint = args.kafka_endpoint
        self.http_endpoint = args.http_endpoint
        #self.amqp_endpoint = args.amqp_endpoint
        self.topic = args.topic
        self.filter = args.filter 
        #self.opaque = args.opaque
        #self.exchange = args.exchange
        self.notification = args.notification
       
        self.s3 = boto3.client('s3',
                              endpoint_url = self.endpoint_url,
                              aws_access_key_id = self.access_key,
                              aws_secret_access_key = self.secret_key,
                              region_name = 'default',
                              config=botocore.client.Config(signature_version = 's3'))
        
        self.attributes = {}


    ''' This function configures bucket notification for object creation and removal '''
    def configure_bucket_notification(self): 
        
        # creates a bucket if it doesn't exists
        try: 
            self.s3.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError:
            self.s3.create_bucket(Bucket = self.bucket_name)

        # initial dictionary 
        bucket_notifications_configuration = {
            "TopicConfigurations": [
                {
                    "Id": self.notification,
                    "TopicArn": attributes['http-endpoint'],
                    "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
                }
            ]
        }
        
        # in case the user has provided a filter to use 
        if(self.filter):
            bucket_notifications_configuration['TopicConfigurations'][0].update({'Filter': json.loads(self.filter)})

        # pushed the notification configuration to the bucket 
        response = self.s3.put_bucket_notification_configuration(Bucket = self.bucket_name, NotificationConfiguration=bucket_notifications_configuration)
        print(response)
        return 

if __name__ == '__main__':
		
    # creates an notifier instance from class
    notifier = Notifier()
		
    # create sns-like topic sent to MQ endpoint 
    #notifier.create_sns_topic()
		
    # configures object creation and removal based notification for the bucket
    notifier.configure_bucket_notification()
