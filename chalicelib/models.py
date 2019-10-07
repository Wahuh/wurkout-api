import boto3
from .db import connection
import uuid
import json
from decimal import Decimal

_users_table = connection.Table("users")
_runs_table = connection.Table("runs")
_followers_table = connection.Table("followers")
_subscriptions_table = connection.Table("subscriptions")
_connections_table = connection.Table("connections")


class User:
    @staticmethod
    def add_one(username):
        new_user_item = {
            'username': username,
            'cumulative_distance': 0,
            'followers': [],
            'subscriptions': []
        }
        try:
            put_user_response = _users_table.put_item(Item=new_user_item)
            print(put_user_response, f'new user inserted {new_user_item}')
            return new_user_item
        except Exception as e:
            raise e
    
    # @staticmethod
    # def update_one(username, first_name, last_name, age, height, weight):
    #         'first_name': first_name,
    #         'last_name': last_name,
    #         'age': age,
    #         'height': height,
    #         'weight': weight,
            

    @staticmethod
    def scan_users(start_username=None):
        try:
            scan_response = None
            if start_username:
                scan_response = _users_table.scan(
                    TableName='users',
                    Limit=10,
                    ExclusiveStartKey={"username": start_username}
                )
            else:
                scan_response = _users_table.scan(
                    TableName='users',
                    Limit=10
                )
            users = scan_response["Items"]
            last_username = None
            if "LastEvaluatedKey" in scan_response:
                if "username" in scan_response["LastEvaluatedKey"]:
                    last_username = scan_response["LastEvaluatedKey"]["username"]
            new_response = {
                "users": users,
                "last_username": last_username
            }
            return new_response
        except Exception as e:
            raise e


class Run:
    @staticmethod
    def add_one(
        username,
        start_time
    ):
        new_run_id = str(uuid.uuid4())
        new_run_item = {
            'run_id': new_run_id,
            'username': username,
            'start_time': start_time
        }
        try:
            put_run_response = _runs_table.put_item(Item=new_run_item)
            print(put_run_response, f'run inserted {new_run_item}')
            return new_run_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(run_id, username, finish_time, average_speed, total_distance):
        try:
            patch_run_response = _runs_table.update_item(
                TableName='runs',
                Key={
                    'username': username,
                    'run_id': run_id
                },
                UpdateExpression='SET finish_time=:finish, average_speed=:average, total_distance=:distance',
                ExpressionAttributeValues={
                    ':finish': {"S": finish_time},
                    ':average': {"N": average_speed},
                    ':distance': {"N": total_distance},
                },
                ReturnValues="ALL_NEW"
            )
            print(patch_run_response)
            return patch_run_response
        except Exception as e:
            raise e


class Followers:
    @staticmethod
    def add_one(
        username,
        follower
    ):
        new_follower_item = {
            'username': username,
            'followers': [follower]
        }
        try:
            put_followers_response = _followers_table.put_item(Item=new_follower_item)
            print(put_followers_response, f'inserted new follower: {new_follower_item}')
            return new_follower_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(username, follower):
        try:
            patch_follower_response = _followers_table.update_item(
                TableName='followers',
                Key={
                    'username': username
                },
                UpdateExpression="SET followers = list_append(followers, :followers)",
                ExpressionAttributeValues={
                    ':followers': {"L": [{"S": follower}]},
                },
                ReturnValues="ALL_NEW"
            )
            print(patch_follower_response)
            return patch_follower_response
        except Exception as e:
            raise e


class Subscriptions:
    @staticmethod
    def add_one(
        username,
        subscription
    ):
        new_subscription_item = {
            'username': username,
            'subscriptions': [subscription]
        }
        try:
            put_subscription_response = dynamodb_resource.Table('subscriptions').put_item(Item=new_subscription_item)
            print(put_subscription_response, f'inserted new subscription {new_subscription_item}')
            return new_subscription_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(
        username,
        subscription
    ):
        try:
            patch_subscription_response = dynamodb_client.update_item(
                TableName='subscriptions',
                Key={
                    'username': {
                        'S': username
                    }
                },
                UpdateExpression="SET subscriptions = list_append(subscriptions, :subscriptions)",
                ExpressionAttributeValues={
                    ':subscriptions': {"L": [{"S": subscription}]},
                },
                ReturnValues="ALL_NEW"
            )
            return patch_subscription_response
        except Exception as e:
            raise e


class Connection:
    @staticmethod
    def add_one(username):
        try:
            new_connection_item = {"username": username}
            put_connection_response = _connections_table.put_item(Item=new_connection_item)
            return put_connection_response
        except Exception as e:
            raise e
    
    @staticmethod
    def add_connection_id(username, connection_id):
        try:
            updated_connection_response = _connections_table.update_item(
                TableName="connections",
                Key={
                    'username': username
                },
                UpdateExpression="SET connection_id=:connection",
                ExpressionAttributeValues={
                    ':connection': {"S": connection_id}
                },
                ReturnValues="ALL_NEW"
            )
            return updated_connection_response
        except Exception as e:
            raise e