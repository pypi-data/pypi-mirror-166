# quick function to role chain into a child account
# can use as standalone or within loop to perform operations each child assoc w/ acct profile"
# uses parent account of pre-configured profile
import boto3

def role_chain(profile, role, child_account):
    from fhaws.org import getaccounts
    acctlist = getaccounts(profile)
    for acct in acctlist:
        if (acct['Name']) == child_account:
            child_account_id = (acct['Id'])
        elif (acct['Id']) == child_account:
            child_account_id = child_account
    
    session = boto3.Session(profile_name=profile)
    sts_client = session.client("sts")
    assumed_role_object = sts_client.assume_role(
            RoleArn=str("arn:aws:iam::" + child_account_id + ":role/" + role),
            RoleSessionName="AssumeRoleSession")
    newsession_id = assumed_role_object['Credentials']['AccessKeyId']
    newsession_key = assumed_role_object['Credentials']['SecretAccessKey']
    newsession_token = assumed_role_object['Credentials']['SessionToken']

    return newsession_id, newsession_key, newsession_token
