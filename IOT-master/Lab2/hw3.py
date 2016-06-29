TableName = "user3"
if_new_table = 0
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
if if_new_table:
	this_table = Table.create(TableName, schema=[HashKey('Name'),RangeKey('CUID')],connection=client_dynamo )
	print("Creating table, please wait...")
else:
	this_table = Table(TableName, connection=client_dynamo )
	print("Reading table, please wait...")

time.sleep(15)

print("Please input your command like one of this,")
print("ADD (Name) (CUID)")
print("DELETE (Name) (CUID)")
print("SEARCH (Name or CUID)")
print("VIEW")
print("EXIT")

command_str = "NONE"
while command_str != "EXIT":
	command_str = raw_input(">>>>")
	cmd_keyword = command_str.partition(" ")[0];
	if cmd_keyword == "ADD":
		this_table.put_item(data={
	     'Name': command_str.split(" ")[1] ,
	     'CUID': command_str.split(" ")[2] 
		})
	elif cmd_keyword == "DELETE":
		this_table.delete_item(Name=command_str.split(" ")[1], CUID=command_str.split(" ")[2])
	elif cmd_keyword == "VIEW":
		all_items = this_table.scan()
		for item in all_items:
			print(item['Name'] + " " + item['CUID'])
	elif cmd_keyword == "SEARCH":
		target_items_Name = this_table.query_2(Name__eq = command_str.split(" ")[1])

		target_items_CUID = []
		all_items = this_table.scan()
		for item in all_items:
			if item["CUID"] == command_str.split(" ")[1]:
				target_items_CUID.append(item)

		if target_items_Name:
			for item in target_items_Name:
				print("Search with Name, Corresponding CUID: " + item["CUID"])
		if target_items_CUID:
			for item in target_items_CUID:
				print("Search with CUID, Corresponding Name: " + item["Name"])















