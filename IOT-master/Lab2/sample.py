 
import boto
import boto.dynamodb2
import time
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


client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)
 
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
users = Table.create('user2', schema=[HashKey('name'),RangeKey('CUID')],connection=client_dynamo )
#users = Table('users',connection=client_dynamo)
time.sleep(15)
users.put_item(data={
     'name': 'Mia',
     'CUID': 'N'
})
