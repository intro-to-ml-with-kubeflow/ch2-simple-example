
import boto3
import logging
import os
import pickle

BUCKET_NAME=os.getenv("BUCKET_NAME")
MODEL_KEY_NAME=os.getenv("MODEL_KEY_NAME")
ACCESS_KEY_ID=os.getenv("S3_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("S3_SECRET_KEY")
REGION_NAME=os.getenv("REGION_NAME")
ENDPOINT_URL=os.getenv("ENDPOINT_URL")

if ACCESS_KEY_ID=="":
    logging.error("Need to set ACCESS_KEY_NAME dumb dumb")
    exit(1)
if ACCESS_KEY_ID is None:
    logging.error("Need to set ACCESS_KEY_NAME dummy")
    exit(1)


class SimpleModel(object):
    def __init__(self):

        logging.warning("Attemptiong to download %s from %s bucket to %s" % (MODEL_KEY_NAME, BUCKET_NAME, './model.pkl'))
        s3 = boto3.resource(
        service_name= 's3',
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_KEY,
        )
        s3.Bucket(BUCKET_NAME).download_file(MODEL_KEY_NAME, './model.pkl')
        with open('./model.pkl', 'rb') as f:
            self.clf = pickle.load(f)
        logging.warning("Great success in retrieving model!!")

    def predict(self,X):
        prediction = self.clf.predict(X)
        return prediction
