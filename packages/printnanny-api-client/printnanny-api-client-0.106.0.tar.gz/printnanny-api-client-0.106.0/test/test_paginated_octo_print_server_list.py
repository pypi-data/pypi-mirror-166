# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.106.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.paginated_octo_print_server_list import PaginatedOctoPrintServerList  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestPaginatedOctoPrintServerList(unittest.TestCase):
    """PaginatedOctoPrintServerList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedOctoPrintServerList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.paginated_octo_print_server_list.PaginatedOctoPrintServerList()  # noqa: E501
        if include_optional :
            return PaginatedOctoPrintServerList(
                count = 123, 
                next = 'http://api.example.org/accounts/?page=4', 
                previous = 'http://api.example.org/accounts/?page=2', 
                results = [
                    printnanny_api_client.models.octo_print_server.OctoPrintServer(
                        id = 56, 
                        settings = null, 
                        base_path = '', 
                        venv_path = '', 
                        pip_path = '', 
                        python_path = '', 
                        octoprint_version = '', 
                        pip_version = '', 
                        python_version = '', 
                        printnanny_plugin_version = '', 
                        created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        user = 56, 
                        pi = 56, )
                    ]
            )
        else :
            return PaginatedOctoPrintServerList(
        )

    def testPaginatedOctoPrintServerList(self):
        """Test PaginatedOctoPrintServerList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
