#this file is work in progress 
#here for the reference only 


import VzCloudCompute
import string, random, datetime, time, hmac, hashlib, base64, requests, json, getpass, sys
from termcolor import colored, cprint
import requests
import timeit
import time

import boto
import boto.s3.connection

import os, math
import getpass
from filechunkio import FileChunkIO
from multiprocessing import Pool

import threading
from threading import Thread, Lock


chassis_url_S3 = "xxxxx.cloud.verizon.com"
accessKey_S3 = "xxxxxxxxxx"
secretKey_S3 = "xxxxxxxxxxxxxxxxxxxxxxx4"


conn = boto.connect_s3(
                aws_access_key_id = accessKey_S3,
                aws_secret_access_key = secretKey_S3,
                host = chassis_url_S3,
                #is_secure=False,               # uncomment if you are not using ssl
                calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                )
print "connection created :", conn, "\n"


for bucket in conn.get_all_buckets():
                print "{name}\t{created}".format(
                                name = bucket.name,
                                created = bucket.creation_date,
                )
                for key in bucket.list():
                        print "{name}\t{size}\t{modified}".format(
                                name = key.name,
                                size = key.size,
                                modified = key.last_modified,
                                )

print "print buckets done \n "
raw_input('enter to continue >')
print  getpass.getuser()
print "script running on", os.path.abspath(__file__)
print "working directory ", os.getcwd()


b = conn.get_bucket('sergeyprod')
key = b.get_key('testfile')


key.get_contents_to_filename('/Users/v671145/Documents/github/api/compute/python/testfile')
key.set_contents_from_filename ('/Users/v671145/Documents/github/api/compute/python/testfile' )
print os.listdir ('/Users/v671145/Documents/github/api/compute/python/')
print "get  testfile done \n "

#create file 'hello.txt' and put the string ito it
b.delete_key('hello.txt') ## does not delete if it is not there
keyN = b.new_key('hello.txt')
keyN.set_contents_from_string('Hello World!')
#not supported by VZ
# CannedACLStrings = ['private', 'public-read', 'project-private', 'public-read-write', 'authenticated-read', 'bucket-owner-read', 'bucket-owner-full-control']
#keyN.set_canned_acl('public-read')
#keyN.set_canned_acl('private')
#keyN.set_canned_acl('bucket-owner-full-control')
#keyN.set_acl('private')

#get and print keys
hello_url = keyN.generate_url(0, query_auth=False, force_http=True)
print hello_url
plans_url = keyN.generate_url(3600, query_auth=True, force_http=True)
print plans_url


# Get file info
source_path = '/Users/v671145/Documents/github/api/compute/python/test_mlt'
source_size = os.stat(source_path).st_size
print 'source_path, source_size', source_path, source_size, ' bytes'

# Create a multipart upload request
mp = b.initiate_multipart_upload(os.path.basename(source_path))
print 'mp', mp

# Use a chunk size of 50 ?? MiB (feel free to change this)
chunk_size = 52428800
chunk_count = int(math.ceil(source_size / chunk_size))
print 'chunk_size, chunk_count', chunk_size, chunk_count


# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
for i in range(chunk_count + 1):
         offset = chunk_size * i
         bytes = min(chunk_size, source_size - offset)
         print "offset",offset
         print "bytes",bytes
         with FileChunkIO(source_path, 'r', offset=offset,
                                                 bytes=bytes) as fp:
                 print "part_num", i+1
                 mp.upload_part_from_file(fp, part_num=i + 1)
                 print "fp", fp

# Finish the upload
mp.complete_upload()
print "fp", fp
print 'mp', mp, "multiPart single threaded Done "

userC = raw_input('> Hold it ..')

#thread it boto way :)
parallel_processes = 20

chunk_size = 52428800
source_path = '/Users/v671145/Documents/github/api/compute/python/test_mltL'
source_size = os.stat(source_path).st_size
chunk_count = int(math.ceil(source_size / chunk_size))
print 'chunk_size, chunk_count', chunk_size, chunk_count


pool = Pool(processes=parallel_processes)


print "start time .................................."
start = time.time()
max_part = chunk_count+1

##CntLst = [CntObj]#prepare to pass by "reference"
for i in range(chunk_count+1):
                #print "loop"
                offset = i * chunk_size
                remaining_bytes = source_size - offset
                bytes = min([chunk_size, remaining_bytes])
                part_num = i + 1
                #print "..... part_num in Pool async ",   part_num

                pool.apply_async(__upload_part, [b, accessKey_S3, secretKey_S3, mp.id,
                                                                                part_num, max_part, source_path, offset, bytes,
                                                                                1, None, 4])


pool.close()
pool.join()
mmmp = len(mp.get_all_parts())
print ".....", mmmp
if len(mp.get_all_parts()) == chunk_count+1:
                mp.complete_upload()
                print "...new way to finish "

end = time.time()
print "mesured ................  = ",   end - start
print 'mp', mp, "multiPart Multi threaded Done "



#FileChunkIO
userC = raw_input('> Hold it ..')
