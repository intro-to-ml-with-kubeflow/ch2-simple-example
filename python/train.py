# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
#     specific language governing permissions and limitations
# under the License.

import argparse
import boto3
import logging
import os
import pandas as pd
from sklearn.linear_model import LinearRegression


BUCKET_NAME=os.getenv("BUCKET_NAME")
MODEL_KEY_NAME=os.getenv("MODEL_KEY_NAME")
ACCESS_KEY=os.getenv("S3_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("S3_SECRET_KEY")

REGION_NAME=os.getenv("REGION_NAME")
ENDPOINT_URL=os.getenv("ENDPOINT_URL")

def read_local(filename):
    """
    Read the data from a file that was coppied to the Docker container durring container creation (probably only useful
    in edge cases, but still informative).
    :param filename: A string, the name and location of the training file.
    :return: A Pandas dataframe of the read data.
    """
    df = pd.read_csv(filename)
    return(df)

def read_s3(s3path):
    data_bucket = s3path.split("/")[2]
    key = "/".join(s3path.split("/")[3:])
    fname = s3path.split("/")[-1]
    logging.info("Attemptiong to download %s from %s bucket to %s" % (key, data_bucket, fname))
    s3 = boto3.resource(
        service_name= 's3',
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3.Bucket(data_bucket).download_file(key, fname)
    df = pd.read_csv(fname)
    return df

def read_http(url):
    """
    Read the data from a url.
    :param url: A string, the url where you want to get the data from. Eg. "https://raw.githubusercontent.com/intro-to-ml-with-kubeflow/ch2-simple-example/master/data/cereal.csv"
    :return: A Pandas dataframe of the read data.
    """
    import requests
    from io import StringIO
    r = requests.get(url)
    data = StringIO(r.text)
    df = pd.read_csv(data)
    return(df)


def train(df):
    xcols = ['protein', 'fat', 'carbo', 'sugars'] #todo make these a passed arg
    ycol = 'rating'
    X = df[xcols]
    y = df[ycol]
    ## NOTE: You could (should) do some train/test splits here but the data set is too small so /shrug
    clf = LinearRegression()
    logging.info("Training linear regression model")
    clf.fit(X, y)
    return clf

def save_model(clf):
    """
    Save Model to S3 (in the future could save to other places too...)
    :return:
    """
    import pickle as pkl
    logging.info("Saving model %s" % MODEL_KEY_NAME + '.pkl')
    with open("model.pkl", 'wb') as f:
        pkl.dump(clf, f)
    # Get the service client
    s3 = boto3.client(
        service_name= 's3',
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    # Upload tmp.txt to bucket-name at key-name
    ## Todo update these
    bucket_name = BUCKET_NAME
    key_name = MODEL_KEY_NAME
    s3.upload_file("model.pkl", bucket_name, key_name)
    return True



def main(args):
    if args.train_input.startswith("http"):
        logging.info("Loading url %s" % args.train_input)
        df = read_http(args.train_input)
    elif args.train_input.startswith("s3"):
        logging.info("Loading %s from S3 Source" % args.train_input)
        df = read_s3(args.train_input)
    else:
        logging.info("Loading local file: %s" % args.train_input)
        df = read_local(args.train_input)
    logging.info("File Loaded successfully...")
    clf = train(df)
    save_model(clf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--train-input',
        help="Input training file",

        required=True
    )

    logging.basicConfig(format='%(message)s')
    logging.getLogger().setLevel(logging.INFO)
    main_args = parser.parse_args()
    main(main_args)