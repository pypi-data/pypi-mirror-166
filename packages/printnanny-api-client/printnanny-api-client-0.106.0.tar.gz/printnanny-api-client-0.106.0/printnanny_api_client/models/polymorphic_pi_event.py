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


class PolymorphicPiEvent(object):
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
        'id': 'str',
        'created_dt': 'datetime',
        'subject_pattern': 'PiBootCommandSubjectPatternEnum',
        'payload': 'dict(str, object)',
        'event_type': 'PiBootCommandType',
        'pi': 'int',
        'version': 'str'
    }

    attribute_map = {
        'id': 'id',
        'created_dt': 'created_dt',
        'subject_pattern': 'subject_pattern',
        'payload': 'payload',
        'event_type': 'event_type',
        'pi': 'pi',
        'version': 'version'
    }

    discriminator_value_class_map = {
    }

    def __init__(self, id=None, created_dt=None, subject_pattern=None, payload=None, event_type=None, pi=None, version=None, local_vars_configuration=None):  # noqa: E501
        """PolymorphicPiEvent - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_dt = None
        self._subject_pattern = None
        self._payload = None
        self._event_type = None
        self._pi = None
        self._version = None
        self.discriminator = 'subject_pattern'

        if id is not None:
            self.id = id
        if created_dt is not None:
            self.created_dt = created_dt
        self.subject_pattern = subject_pattern
        self.payload = payload
        self.event_type = event_type
        self.pi = pi
        self.version = version

    @property
    def id(self):
        """Gets the id of this PolymorphicPiEvent.  # noqa: E501


        :return: The id of this PolymorphicPiEvent.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PolymorphicPiEvent.


        :param id: The id of this PolymorphicPiEvent.  # noqa: E501
        :type id: str
        """

        self._id = id

    @property
    def created_dt(self):
        """Gets the created_dt of this PolymorphicPiEvent.  # noqa: E501


        :return: The created_dt of this PolymorphicPiEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this PolymorphicPiEvent.


        :param created_dt: The created_dt of this PolymorphicPiEvent.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def subject_pattern(self):
        """Gets the subject_pattern of this PolymorphicPiEvent.  # noqa: E501


        :return: The subject_pattern of this PolymorphicPiEvent.  # noqa: E501
        :rtype: PiBootCommandSubjectPatternEnum
        """
        return self._subject_pattern

    @subject_pattern.setter
    def subject_pattern(self, subject_pattern):
        """Sets the subject_pattern of this PolymorphicPiEvent.


        :param subject_pattern: The subject_pattern of this PolymorphicPiEvent.  # noqa: E501
        :type subject_pattern: PiBootCommandSubjectPatternEnum
        """
        if self.local_vars_configuration.client_side_validation and subject_pattern is None:  # noqa: E501
            raise ValueError("Invalid value for `subject_pattern`, must not be `None`")  # noqa: E501

        self._subject_pattern = subject_pattern

    @property
    def payload(self):
        """Gets the payload of this PolymorphicPiEvent.  # noqa: E501


        :return: The payload of this PolymorphicPiEvent.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this PolymorphicPiEvent.


        :param payload: The payload of this PolymorphicPiEvent.  # noqa: E501
        :type payload: dict(str, object)
        """

        self._payload = payload

    @property
    def event_type(self):
        """Gets the event_type of this PolymorphicPiEvent.  # noqa: E501


        :return: The event_type of this PolymorphicPiEvent.  # noqa: E501
        :rtype: PiBootCommandType
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this PolymorphicPiEvent.


        :param event_type: The event_type of this PolymorphicPiEvent.  # noqa: E501
        :type event_type: PiBootCommandType
        """
        if self.local_vars_configuration.client_side_validation and event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `event_type`, must not be `None`")  # noqa: E501

        self._event_type = event_type

    @property
    def pi(self):
        """Gets the pi of this PolymorphicPiEvent.  # noqa: E501


        :return: The pi of this PolymorphicPiEvent.  # noqa: E501
        :rtype: int
        """
        return self._pi

    @pi.setter
    def pi(self, pi):
        """Sets the pi of this PolymorphicPiEvent.


        :param pi: The pi of this PolymorphicPiEvent.  # noqa: E501
        :type pi: int
        """
        if self.local_vars_configuration.client_side_validation and pi is None:  # noqa: E501
            raise ValueError("Invalid value for `pi`, must not be `None`")  # noqa: E501

        self._pi = pi

    @property
    def version(self):
        """Gets the version of this PolymorphicPiEvent.  # noqa: E501


        :return: The version of this PolymorphicPiEvent.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PolymorphicPiEvent.


        :param version: The version of this PolymorphicPiEvent.  # noqa: E501
        :type version: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                version is not None and len(version) > 32):
            raise ValueError("Invalid value for `version`, length must be less than or equal to `32`")  # noqa: E501

        self._version = version

    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_key = self.attribute_map[self.discriminator]
        discriminator_value = data[discriminator_key]
        return self.discriminator_value_class_map.get(discriminator_value)

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
        if not isinstance(other, PolymorphicPiEvent):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PolymorphicPiEvent):
            return True

        return self.to_dict() != other.to_dict()
