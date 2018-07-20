import boto3
import uuid
from time import sleep
from pprint import pprint
from botocore.exceptions import ClientError

class S3():
    def __init__(self, bucket):
        self.client = boto3.client("s3")
        self.s3 = boto3.resource("s3")
        self.bucket = bucket

    def ls(self):
        d = self.client.list_objects(Bucket=self.bucket)
        print(d)
        return d
    
    def rm(self, key):
        d = self.client.delete_object(
            Bucket=self.bucket,
            Key=key
        )
        return d
    
    def make_public(self, key):
        return self.s3.ObjectAcl(self.bucket, key).put(ACL='public-read')


if __name__=="__main__":
    # from botomod import S3; s3 = S3("nrel-nwtc-metmast-uni"); d = s3.ls()
    s3 = S3("nrel-nwtc-metmast-uni")
    # d = s3.ls()
    # d["Contents"]
    # d = s3.rm("/int/moby_dick.html")
    # d = s3.rm("/int/2017_January.csv")
    # print(d)
    print(s3.make_public("int/dt=2017-01/2017_January.csv"))


# class Athena():
#     def __init__(self):
#         self.client = boto3.client("athena", "us-west-2")

#     def run_query(self, sql, database, output_bucket):
#         response = self.client.start_query_execution(
#             QueryString=sql,
#             #ClientRequestToken=uuid._uuid_generate_random,
#             QueryExecutionContext={
#                 'Database': database
#             },
#             ResultConfiguration={
#                 'OutputLocation': "s3://" + output_bucket,

#                 'EncryptionConfiguration': {
#                     'EncryptionOption': 'SSE_S3'
#                 }
#             }
#         )

#         #pprint(response)

#         queryId = response["QueryExecutionId"]

#         response = self.client.list_named_queries(
#             #NextToken=nextToken,
#             MaxResults=10
#         )

#         #pprint(response)

#         isQueryStillRunning = True
#         nextToken = None
#         while isQueryStillRunning:
#             try:
#                 response = self.client.get_query_results(
#                     QueryExecutionId=queryId,
#                     #NextToken='string',
#                     #MaxResults=123
#                 )
#                 #pprint(response)
#                 return response["ResultSet"]


#             except ClientError as e:
#                 #print e.response

#                 if "RUNNING" in e.response['Error']['Message'] or "QUEUED" in e.response['Error']['Message']:
#                     print("Query still running.  Polling for results.")
#                     sleep(1)
#                 else:
#                     print (e.response)
#                     print ("Unexpected error: %s" % e)
