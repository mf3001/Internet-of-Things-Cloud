import boto
from boto import kinesis
import json

ACCOUNT_ID = '486153037878'
IDENTITY_POOL_ID = 'us-east-1:343fd9ae-5dbb-4a98-994d-d0a0fd0cfee1'
ROLE_ARN = 'arn:aws:iam::486153037878:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# Prepare Kinesis client
client_kinesis = boto.connect_kinesis(
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

#kinesis = client_kinesis.create_stream("IOT_temp",1)
client_kinesis.put_record("IOT_temp",json.dumps('a b'),"partitionkey")
shard_id = 'shardId-000000000000' #we only have one shard!
shard_it = client_kinesis.get_shard_iterator("IOT_temp", shard_id, 
"LATEST")["ShardIterator"]
out = client_kinesis.get_records(shard_it, limit=25)
print out

