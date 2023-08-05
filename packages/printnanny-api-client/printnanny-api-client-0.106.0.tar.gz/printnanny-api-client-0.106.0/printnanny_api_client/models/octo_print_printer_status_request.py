# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.106.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class OctoPrintPrinterStatusRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'subject_pattern': 'OctoPrintPrinterStatusSubjectPatternEnum',
        'payload': 'dict(str, object)',
        'event_type': 'OctoPrintPrinterStatusType',
        'octoprint_server': 'int',
        'pi': 'int'
    }

    attribute_map = {
        'subject_pattern': 'subject_pattern',
        'payload': 'payload',
        'event_type': 'event_type',
        'octoprint_server': 'octoprint_server',
        'pi': 'pi'
    }

    def __init__(self, subject_pattern=None, payload=None, event_type=None, octoprint_server=None, pi=None, local_vars_configuration=None):  # noqa: E501
        """OctoPrintPrinterStatusRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._subject_pattern = None
        self._payload = None
        self._event_type = None
        self._octoprint_server = None
        self._pi = None
        self.discriminator = None

        self.subject_pattern = subject_pattern
        self.payload = payload
        self.event_type = event_type
        self.octoprint_server = octoprint_server
        self.pi = pi

    @property
    def subject_pattern(self):
        """Gets the subject_pattern of this OctoPrintPrinterStatusRequest.  # noqa: E501


        :return: The subject_pattern of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :rtype: OctoPrintPrinterStatusSubjectPatternEnum
        """
        return self._subject_pattern

    @subject_pattern.setter
    def subject_pattern(self, subject_pattern):
        """Sets the subject_pattern of this OctoPrintPrinterStatusRequest.


        :param subject_pattern: The subject_pattern of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :type subject_pattern: OctoPrintPrinterStatusSubjectPatternEnum
        """
        if self.local_vars_configuration.client_side_validation and subject_pattern is None:  # noqa: E501
            raise ValueError("Invalid value for `subject_pattern`, must not be `None`")  # noqa: E501

        self._subject_pattern = subject_pattern

    @property
    def payload(self):
        """Gets the payload of this OctoPrintPrinterStatusRequest.  # noqa: E501


        :return: The payload of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this OctoPrintPrinterStatusRequest.


        :param payload: The payload of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :type payload: dict(str, object)
        """

        self._payload = payload

    @property
    def event_type(self):
        """Gets the event_type of this OctoPrintPrinterStatusRequest.  # noqa: E501


        :return: The event_type of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :rtype: OctoPrintPrinterStatusType
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this OctoPrintPrinterStatusRequest.


        :param event_type: The event_type of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :type event_type: OctoPrintPrinterStatusType
        """
        if self.local_vars_configuration.client_side_validation and event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `event_type`, must not be `None`")  # noqa: E501

        self._event_type = event_type

    @property
    def octoprint_server(self):
        """Gets the octoprint_server of this OctoPrintPrinterStatusRequest.  # noqa: E501


        :return: The octoprint_server of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :rtype: int
        """
        return self._octoprint_server

    @octoprint_server.setter
    def octoprint_server(self, octoprint_server):
        """Sets the octoprint_server of this OctoPrintPrinterStatusRequest.


        :param octoprint_server: The octoprint_server of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :type octoprint_server: int
        """
        if self.local_vars_configuration.client_side_validation and octoprint_server is None:  # noqa: E501
            raise ValueError("Invalid value for `octoprint_server`, must not be `None`")  # noqa: E501

        self._octoprint_server = octoprint_server

    @property
    def pi(self):
        """Gets the pi of this OctoPrintPrinterStatusRequest.  # noqa: E501


        :return: The pi of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :rtype: int
        """
        return self._pi

    @pi.setter
    def pi(self, pi):
        """Sets the pi of this OctoPrintPrinterStatusRequest.


        :param pi: The pi of this OctoPrintPrinterStatusRequest.  # noqa: E501
        :type pi: int
        """
        if self.local_vars_configuration.client_side_validation and pi is None:  # noqa: E501
            raise ValueError("Invalid value for `pi`, must not be `None`")  # noqa: E501

        self._pi = pi

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OctoPrintPrinterStatusRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OctoPrintPrinterStatusRequest):
            return True

        return self.to_dict() != other.to_dict()
