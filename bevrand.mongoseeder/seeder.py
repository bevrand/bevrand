#!/usr/bin/env python

from pymongo import MongoClient
import psycopg2
import glob
import json


#CONNECTION = 'mongodb://localhost:27017'
CONNECTION = 'mongodb://dockermongo:27017'


def connect_postgres():
    conn = psycopg2.connect("user='postgres' dbname='postgres' host='dockergres' password='postgres' port='5432'")
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("CREATE TABLE users(id BIGSERIAL PRIMARY KEY NOT NULL, "
                "username VARCHAR(50) NOT NULL, "
                "password VARCHAR(250) NOT NULL,"
                "email VARCHAR(60),"
                "active BOOLEAN NOT NULL,"
                "datecreated TIMESTAMP,"
                "dateupdated TIMESTAMP)")
    cur.execute("CREATE UNIQUE INDEX users_username_uindex ON users (username)")



def insert_collections():
    connectionstring = CONNECTION
    client = MongoClient(connectionstring)
    db = client.bevrand
    postids = []
    files = get_json_files()
    for file in files:
        if file == "./users.json":
            postids = insert_specific_collection(file, db.users)
        else:
            postids = insert_specific_collection(file, db.frontpagestandard)
    return postids


def insert_specific_collection(file, col):
    post_ids = []
    with open(file) as data_file:
        data = json.load(data_file)
    for d in data:
        print(d)
        try:
            post_id = col.insert_one(d).inserted_id
            post_ids.append(post_id)
        except:
            print("error!")
    return post_ids


def get_json_files():
    path = './*.json'
    files = glob.glob(path)
    return files


print("Starting to import")
jsonfiles = get_json_files()
for file in jsonfiles:
    print("Going to import the following file: " + file)
ids = insert_collections()
print(ids)
connect_postgres()
print("finished run")


