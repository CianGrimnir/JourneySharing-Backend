from botocore.exceptions import ClientError
from enum import Enum, unique
from typing import List
from services.response import ServicesApiResponse
from services import const
import boto3


class Service:
    """
    This class acts as a base to other services to capture common
    functionality.

    services are classes that wrap other classes to provide higher-level
    abstractions.

    Attributes:
        NOT_READY_RESPONSE  A single CloudServicesApiResponse that models
        the case where the Manager is not ready to service requests.
    """

    @unique
    class Response(Enum):
        """
        Contains common response constants.
        """
        OK = (0, 'OK')
        UNAVAILABLE = (1, 'UNAVAILABLE')

        def __init__(self, return_code: int, reason: str = None):
            """
            Constructs the Response.

            :param return_code: The integer return code that represents the
            common response.

            :param reason: A simple text string that provides a simple
            explanation of the response.
            """
            if return_code is None:
                raise ValueError('response return code is required')
            self.return_code = return_code
            if reason is None:
                raise ValueError('response reason is required')
            self.reason = reason

        def __str__(self):
            return str(self.__dict__)

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __repr__(self):
            return str(self.__dict__)

    def __init__(self, service_name: str = None, region: str = const.default_region, aws_service_key: str = const.AWS_ACCESS_KEY_ID,
                 aws_secret_key: str = const.AWS_SECRET_ACCESS_KEY):
        """
        Initializes the Service.

        :param region: The region in which the aws service resides.

        :param aws_service_key: Specifies the AWS access key used as part of the credentials to authenticate the user.

        :param aws_secret_key: credentials to authenticate the AWS user.
        manager.
        """
        self.region = region if region is not None else "default_region"
        self.aws_service_key = aws_service_key if aws_service_key is not None else "AWS_ACCESS_KEY_ID"
        self.aws_secret_key = aws_secret_key if aws_secret_key is not None else "AWS_SECRET_ACCESS_KEY"
        self.service_client = None if service_name is None else \
            boto3.client(**{'service_name': service_name, 'region_name': region, 'aws_access_key_id ': aws_service_key, 'aws_secret_access_key': aws_secret_key})
        self.service_resource = None if service_name is None else \
            boto3.resource(**{'service_name': service_name, 'region_name': region, 'aws_access_key_id ': aws_service_key, 'aws_secret_access_key': aws_secret_key})

    @staticmethod
    def build_ok_response(return_code: int = Response.OK.return_code, reason: str = Response.OK.reason, errors: List[Exception] = None,
                          **kwargs) -> ServicesApiResponse:
        """
         Produces a ServicesApiResponse representing an 'OK' response and
         with the contents of the kwargs.

         :param return_code: The return code for the CloudServicesApiResponse.

         :param reason: A string describing the reason for the return_code.

         :param errors: Any errors that resulted during the generation of the
         ServicesApiResponse.

         :param kwargs: Any additional named parameters provided for the API
         response.

         :return: The ServicesApiResponse that captures all the provided
         arguments.
         """
        return ServicesApiResponse(return_code=return_code, reason=reason, errors=errors, **kwargs)

    @staticmethod
    def build_unavailable_response(return_code: int = Response.UNAVAILABLE.return_code, reason: str = Response.UNAVAILABLE.reason, errors: List[Exception] = None,
                                   **kwargs) -> ServicesApiResponse:
        """
        Produces a ServicesApiResponse representing a 'UNAVAILABLE' response and
        with the contents of the kwargs.

        :param return_code: The return code for the CloudServicesApiResponse.

        :param reason: A string describing the reason for the return_code.

        :param errors: Any errors that resulted during the generation of the
         ServicesApiResponse.

        :param kwargs: Any additional named parameters provided for the API
         response.

        :return: The ServicesApiResponse that captures all the provided
         arguments.
         """
        return ServicesApiResponse(return_code=return_code, reason=reason, errors=errors, **kwargs)

    @staticmethod
    def build_error_response(client_error: ClientError, **kwargs) -> ServicesApiResponse:
        """
        Accepts a boto3 ClientError and builds a CloudServicesApiResponse
        object from it.

        :param client_error: The boto3 ClientError from which the response
        will be built.

        :return: The CloudServicesApiResponse built from client_error.
        """
        return ServicesApiResponse(return_code=client_error.response['ResponseMetadata']['HTTPStatusCode'],
                                   reason=client_error.response['Error']['Code'],
                                   errors=[client_error],
                                   **kwargs)

    def is_ready(self) -> bool:
        """
        Determines whether the Service is ready to handle requests.

        :return: True if the Manager is ready to process requests and false
        otherwise.
        """
        return self.service_resource is not None and self.service_client is not None
