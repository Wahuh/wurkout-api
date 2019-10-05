import boto3
from .db import connection
import uuid

_users_table = connection.Table("users")
_runs_table = connection.Table("runs")
_followers_table = connection.Table("followers")
_subscriptions_table = connection.Table("subscriptions")

print('**************************************************')

# print(boto3.client('dynamodb').list_tables())
dynamodb_resource = boto3.resource("dynamodb")


class User:
    @staticmethod
    def add_one(username, first_name, last_name, age, height, weight):
        new_user_item = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'height': height,
            'weight': weight
        }
        try:
            put_user_response = dynamodb_resource.Table('users').put_item(Item=new_user_item)
            print(put_user_response, f'new user inserted {new_user_item}')
            return new_user_item
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
            # put_run_response = _runs_table.put_item(Item=new_run_item)
            put_run_response = dynamodb_resource.Table("runs").put_item(Item=new_run_item)
            print(put_run_response, f'run inserted {new_run_item}')
            return new_run_item
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
            put_followers_response = dynamodb_resource.Table('followers').put_item(Item=new_follower_item)
            print(put_followers_response, f'inserted new follower: {new_follower_item}')
            return new_follower_item
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
            put_subscription_response = _subscriptions_table.put_item(Item=new_subscription_item)
            print(put_subscription_response, f'inserted new subscription {new_subscription_item}')
            return new_subscription_item
        except Exception as e:
            raise e
