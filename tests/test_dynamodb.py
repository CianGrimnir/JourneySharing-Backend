from unittest.mock import MagicMock
from unittest.mock import patch
from services import const
from services.service import Service
import pytest
import services
from services.dynamodb import DynamoDbService
from decimal import Decimal

scan_table_response_populated = \
    {'Items': [{'user_id': 'testid', 'email': 'asd@dsa.com'}], 'Count': 17, 'ScannedCount': 18,
     'ResponseMetadata': {'RequestId': '6F70V1T4O689II60O6LHF5Q84RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200,
                          'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 15 Mar 2022 08:44:26 UTC', 'content-type': 'application/x-amz-json-1.0', 'content-length': '4938',
                                          'connection': 'keep-alive', 'x-amzn-requestid': '6F70V1T4O689II60O6LHF5Q84RVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '4222624325'},
                          'RetryAttempts': 0}}

scan_table_response_empty = \
    {'Items': [], 'Count': 0, 'ScannedCount': 18, 'ResponseMetadata': {'RequestId': '8MOLOQFTBGKEN98E4NQQKGQ17NVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200,
                                                                       'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 15 Mar 2022 08:44:26 UTC',
                                                                                       'content-type': 'application/x-amz-json-1.0', 'content-length': '40',
                                                                                       'connection': 'keep-alive',
                                                                                       'x-amzn-requestid': '8MOLOQFTBGKEN98E4NQQKGQ17NVV4KQNSO5AEMVJF66Q9ASUAAJG',
                                                                                       'x-amz-crc32': '1157951238'}, 'RetryAttempts': 0}}

get_scan_results_populated = [{'user_id': 'testid', 'email': 'asd@dsa.com'}]
get_scan_results_empty = []

put_table_response_populated = {'ResponseMetadata': {'RequestId': 'GS8BG7QJASQA3VGM88HOAO229NVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200,
                                                     'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 15 Mar 2022 08:44:26 UTC', 'content-type': 'application/x-amz-json-1.0',
                                                                     'content-length': '2', 'connection': 'keep-alive',
                                                                     'x-amzn-requestid': 'GS8BG7QJASQA3VGM88HOAO229NVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'},
                                                     'RetryAttempts': 0}}
put_table_response_populated_exist = "Entry already exists"

get_table_response_populated = {'user_id': 'testid', 'email': 'asd@dsa.com'}
get_table_response_populated_empty = None

get_table_response = {'Item': {'user_id': 'testid', 'email': 'asd@dsa.com'}, 'ResponseMetadata': {'RequestId': 'UHRF5TU22E0VH1GF7HJ34KIEPRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 08 Apr 2019 10:53:50 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '299', 'connection': 'keep-alive', 'x-amzn-requestid': 'UHRF5TU22E0VH1GF7HJ34KIEPRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '793047187'}, 'RetryAttempts': 0}}
get_table_response_empty = {'ResponseMetadata': {'RequestId': 'ASESU77GH5U7CSME2QDG90HCDNVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 15 Mar 2022 08:44:26 UTC', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': 'ASESU77GH5U7CSME2QDG90HCDNVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}


@pytest.mark.parametrize(
    'is_ready, scan_table_response, get_scan_results', [
        (True, scan_table_response_populated, get_scan_results_populated),
        (True, scan_table_response_empty, get_scan_results_empty),
        (False, None, None)
    ]
)
def test_proper_scan_table(is_ready, scan_table_response, get_scan_results):
    service_resource_mock = MagicMock()
    ddb_table_mock = MagicMock()
    ddb_table_mock.scan.return_value = scan_table_response
    service_resource_mock.Table.return_value = ddb_table_mock
    with patch('boto3.session.Session'):
        manager = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        manager.service_resource = service_resource_mock
        manager.is_ready = MagicMock(return_value=is_ready)

        # defining table name  and filter expression and filter expression value
        the_table = 'login_table'
        response = manager.scan_table(the_table, 'filter', 'email')
        services.logger.debug(response)
        if is_ready:
            assert response.return_code == Service.Response.OK.return_code
            assert response.items == get_scan_results
        else:
            assert response.item is None
            if is_ready:
                assert response.return_code == Service.Response.OK.return_code
            else:
                print(response.return_code)
                assert response.return_code == Service.Response.UNAVAILABLE.return_code


@pytest.mark.parametrize(
    'is_ready, put_item_in_table_response', [
        (True, put_table_response_populated),
        (True, put_table_response_populated_exist),
        (False, None)
    ]
)
def test_put_item_in_table(is_ready, put_item_in_table_response):
    service_resource_mock = MagicMock()
    ddb_table_mock = MagicMock()
    ddb_table_mock.put_item.return_value = put_item_in_table_response
    service_resource_mock.Table.return_value = ddb_table_mock

    with patch('boto3.session.Session'):
        manager = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        manager.service_resource = service_resource_mock
        manager.is_ready = MagicMock(return_value=is_ready)
        the_table = "login_table"
        item_data = {
            "userid": "test",
            "email": "test@email.com",
            "phone_number": 123435433212
        }

        response = manager.put_item_in_table(the_table, item_data)
        if is_ready:
            assert response.return_code == Service.Response.OK.return_code
            assert response.item == put_item_in_table_response

        else:
            assert response.return_code == Service.Response.UNAVAILABLE.return_code


@pytest.mark.parametrize(
  'is_ready, get_item_from_table_response, item_from_table', [
    (True, get_table_response, get_table_response_populated),
    (True, get_table_response_empty, get_table_response_populated_empty),
    (False, None, None)
  ]
)
def test_get_table_item(is_ready, get_item_from_table_response, item_from_table):
    # build out the service mocks
    service_resource_mock = MagicMock()
    ddb_table_mock = MagicMock()
    ddb_table_mock.get_item.return_value = get_item_from_table_response
    service_resource_mock.Table.return_value = ddb_table_mock

    with patch('boto3.session.Session'):
        manager = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        manager.service_resource = service_resource_mock

        manager.is_ready = MagicMock(return_value=is_ready)

        the_table = "login_table"
        search_key = {'email': 'asd@dsa.com'}

        response = manager.get_item_from_table(the_table, search_key)
        print("this is response", response)
        if is_ready:
            assert response.return_code == Service.Response.OK.return_code
            assert response.item == item_from_table
        else:
            assert response.return_code == Service.Response.UNAVAILABLE.return_code
            assert response.item is None
