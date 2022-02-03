from botocore.exceptions import ClientError
import services
from .service import Service
from services.response import ServicesApiResponse
from typing import Dict
from boto3.dynamodb.conditions import Key
from services import const


class DynamoDbService(Service):
    """
    This class provides higher-level integration with DynamoDB to facilitate common operations.
    """

    def __init__(self, service_name: str = 'dynamodb', region: str = const.default_region, aws_service_key: str = const.AWS_ACCESS_KEY_ID,
                 aws_secret_key: str = const.AWS_SECRET_ACCESS_KEY):
        """
        Initializes the Service.

        :param region: The region in which the aws service resides.

        :param aws_service_key: Specifies the AWS access key used as part of the credentials to authenticate the user.

        :param aws_secret_key: credentials to authenticate the AWS user.
        manager.
        """
        super().__init__(service_name, region, aws_service_key, aws_secret_key)

    def scan_table(self, table_name: str, filter_name: str, filter_value: str) -> ServicesApiResponse:
        """
        Scan DynamoDB table.

        :param table_name: The DynamoDB table in question.
        :param filter_name: Filter Expression Name.
        :param filter_value: Filter Expression Value.

        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#boto3.dynamodb.conditions.Key

        :return: A ServicesApiError containing the following attributes:
            items - A list of all the matched items from DynamoDB table in Dict format. If
            there is no match then this value will contain an empty list.
        """
        ddb_table = self.service_resource.Table(table_name)
        if not self.is_ready():
            response = Service.build_unavailable_response(**{'item': None})
        else:
            try:
                if table_name is None:
                    item_from_table = None
                else:
                    filtering_exp = Key(filter_name).eq(filter_value)
                    item_from_table = \
                        ddb_table.scan(FilterExpression=filtering_exp)['Items']
                response = \
                    Service.build_ok_response(**{'items': item_from_table})
            except ClientError as e:
                response = Service.build_error_response(e)
        return response

    def put_item_in_table(self, table_name: str, item_data: Dict) -> ServicesApiResponse:
        """
        Inserts items in Dynamodb tables
        :param table_name: The DynamoDB table in question.
        :param item_data: data in the form of dictionary to be inserted in table

        :return: A ServicesApiError containing the following attributes:
        Inserts the values from data provided as input in table.
        Returns exception if data already exists in table
        """
        ddb_table = self.service_resource.Table(table_name)
        if not self.is_ready():
            response = Service.build_unavailable_response(**{'tables': None})
        else:
            try:
                if table_name is None:
                    item_in_table = None
                else:
                    item_in_table = ddb_table.put_item(Item=item_data, Expected={'id': {'Exists': False}})
                response = Service.build_ok_response(**{'item': item_in_table})
            except ClientError as e:
                response = Service.build_error_response(e)
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    services.logger.info("Entry already exists")
                else:
                    services.logger.info(e.response['Error']['Message'])
        return response

    def get_item_from_table(self, table_name: str, search_key: Dict) -> ServicesApiResponse:
        """
        Gets item values for given dynamodb table based on primary key and sort key.
        :param table_name: The DynamoDB table in question.
        :param search_key: dict representing the primary key of the item to retrieve.

        :return: A ServicesApiError containing the following attributes:
        tables - Returns a Dict in key value pair for given search_key value.
        """
        ddb_table = self.service_resource.Table(table_name)
        if not self.is_ready():
            response = Service.build_unavailable_response(**{'tables': None, 'item': None})
        else:
            try:
                if table_name is None:
                    item_from_table = None
                else:
                    item_from_table = ddb_table.get_item(Key=search_key)
                response = Service.build_ok_response(**{'item': item_from_table})
            except ClientError as e:
                response = Service.build_error_response(e)
        return response
