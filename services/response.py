from typing import List, Dict

"""
Defines the elements of the request-response model used within the Cloud Services API.
"""


class ServicesApiResponse:
    """
    Defines a class used to receive responses from within the Services API.
    """

    def __init__(self, return_code: int = 0, reason: str = 'OK', errors: List[Exception] = None, **kwargs):
        """
        Constructs the ServicesApiResponse.

        :param return_code: The return code for the ServicesApiResponse.
         the return code for a successful execution should be 0.

        :param reason: A string describing the reason for the return_code.

        :param errors: Any errors that resulted during the generation of the
        ServicesApiResponse. If no errors with this response, this value should be None.

        :param kwargs: Any additional named parameters provided for the API
        response.
        """

        self.return_code = return_code
        self.reason = reason
        self.errors = errors
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)
