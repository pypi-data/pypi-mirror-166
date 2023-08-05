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


class OctoPrintSettings(object):
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
        'id': 'int',
        'octoprint_enabled': 'bool',
        'events_enabled': 'bool',
        'sync_gcode': 'bool',
        'sync_printer_profiles': 'bool',
        'sync_backups': 'bool',
        'auto_backup': 'str',
        'updated_dt': 'datetime',
        'octoprint_server': 'int'
    }

    attribute_map = {
        'id': 'id',
        'octoprint_enabled': 'octoprint_enabled',
        'events_enabled': 'events_enabled',
        'sync_gcode': 'sync_gcode',
        'sync_printer_profiles': 'sync_printer_profiles',
        'sync_backups': 'sync_backups',
        'auto_backup': 'auto_backup',
        'updated_dt': 'updated_dt',
        'octoprint_server': 'octoprint_server'
    }

    def __init__(self, id=None, octoprint_enabled=None, events_enabled=None, sync_gcode=None, sync_printer_profiles=None, sync_backups=None, auto_backup=None, updated_dt=None, octoprint_server=None, local_vars_configuration=None):  # noqa: E501
        """OctoPrintSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._octoprint_enabled = None
        self._events_enabled = None
        self._sync_gcode = None
        self._sync_printer_profiles = None
        self._sync_backups = None
        self._auto_backup = None
        self._updated_dt = None
        self._octoprint_server = None
        self.discriminator = None

        self.id = id
        if octoprint_enabled is not None:
            self.octoprint_enabled = octoprint_enabled
        if events_enabled is not None:
            self.events_enabled = events_enabled
        if sync_gcode is not None:
            self.sync_gcode = sync_gcode
        if sync_printer_profiles is not None:
            self.sync_printer_profiles = sync_printer_profiles
        if sync_backups is not None:
            self.sync_backups = sync_backups
        if auto_backup is not None:
            self.auto_backup = auto_backup
        self.updated_dt = updated_dt
        self.octoprint_server = octoprint_server

    @property
    def id(self):
        """Gets the id of this OctoPrintSettings.  # noqa: E501


        :return: The id of this OctoPrintSettings.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OctoPrintSettings.


        :param id: The id of this OctoPrintSettings.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def octoprint_enabled(self):
        """Gets the octoprint_enabled of this OctoPrintSettings.  # noqa: E501

        Start OctoPrint service  # noqa: E501

        :return: The octoprint_enabled of this OctoPrintSettings.  # noqa: E501
        :rtype: bool
        """
        return self._octoprint_enabled

    @octoprint_enabled.setter
    def octoprint_enabled(self, octoprint_enabled):
        """Sets the octoprint_enabled of this OctoPrintSettings.

        Start OctoPrint service  # noqa: E501

        :param octoprint_enabled: The octoprint_enabled of this OctoPrintSettings.  # noqa: E501
        :type octoprint_enabled: bool
        """

        self._octoprint_enabled = octoprint_enabled

    @property
    def events_enabled(self):
        """Gets the events_enabled of this OctoPrintSettings.  # noqa: E501

        Send OctoPrint events related to print job status/progress to PrintNanny Cloud https://docs.octoprint.org/en/master/events/index.html  # noqa: E501

        :return: The events_enabled of this OctoPrintSettings.  # noqa: E501
        :rtype: bool
        """
        return self._events_enabled

    @events_enabled.setter
    def events_enabled(self, events_enabled):
        """Sets the events_enabled of this OctoPrintSettings.

        Send OctoPrint events related to print job status/progress to PrintNanny Cloud https://docs.octoprint.org/en/master/events/index.html  # noqa: E501

        :param events_enabled: The events_enabled of this OctoPrintSettings.  # noqa: E501
        :type events_enabled: bool
        """

        self._events_enabled = events_enabled

    @property
    def sync_gcode(self):
        """Gets the sync_gcode of this OctoPrintSettings.  # noqa: E501

        Sync Gcode files to/from PrintNanny Cloud  # noqa: E501

        :return: The sync_gcode of this OctoPrintSettings.  # noqa: E501
        :rtype: bool
        """
        return self._sync_gcode

    @sync_gcode.setter
    def sync_gcode(self, sync_gcode):
        """Sets the sync_gcode of this OctoPrintSettings.

        Sync Gcode files to/from PrintNanny Cloud  # noqa: E501

        :param sync_gcode: The sync_gcode of this OctoPrintSettings.  # noqa: E501
        :type sync_gcode: bool
        """

        self._sync_gcode = sync_gcode

    @property
    def sync_printer_profiles(self):
        """Gets the sync_printer_profiles of this OctoPrintSettings.  # noqa: E501

        Sync Printer Profiles to/from PrintNanny Cloud  # noqa: E501

        :return: The sync_printer_profiles of this OctoPrintSettings.  # noqa: E501
        :rtype: bool
        """
        return self._sync_printer_profiles

    @sync_printer_profiles.setter
    def sync_printer_profiles(self, sync_printer_profiles):
        """Sets the sync_printer_profiles of this OctoPrintSettings.

        Sync Printer Profiles to/from PrintNanny Cloud  # noqa: E501

        :param sync_printer_profiles: The sync_printer_profiles of this OctoPrintSettings.  # noqa: E501
        :type sync_printer_profiles: bool
        """

        self._sync_printer_profiles = sync_printer_profiles

    @property
    def sync_backups(self):
        """Gets the sync_backups of this OctoPrintSettings.  # noqa: E501

        Upload OctoPrint backups to PrintNanny Cloud  # noqa: E501

        :return: The sync_backups of this OctoPrintSettings.  # noqa: E501
        :rtype: bool
        """
        return self._sync_backups

    @sync_backups.setter
    def sync_backups(self, sync_backups):
        """Sets the sync_backups of this OctoPrintSettings.

        Upload OctoPrint backups to PrintNanny Cloud  # noqa: E501

        :param sync_backups: The sync_backups of this OctoPrintSettings.  # noqa: E501
        :type sync_backups: bool
        """

        self._sync_backups = sync_backups

    @property
    def auto_backup(self):
        """Gets the auto_backup of this OctoPrintSettings.  # noqa: E501


        :return: The auto_backup of this OctoPrintSettings.  # noqa: E501
        :rtype: str
        """
        return self._auto_backup

    @auto_backup.setter
    def auto_backup(self, auto_backup):
        """Sets the auto_backup of this OctoPrintSettings.


        :param auto_backup: The auto_backup of this OctoPrintSettings.  # noqa: E501
        :type auto_backup: str
        """
        if (self.local_vars_configuration.client_side_validation and
                auto_backup is not None and len(auto_backup) > 64):
            raise ValueError("Invalid value for `auto_backup`, length must be less than or equal to `64`")  # noqa: E501

        self._auto_backup = auto_backup

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OctoPrintSettings.  # noqa: E501


        :return: The updated_dt of this OctoPrintSettings.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OctoPrintSettings.


        :param updated_dt: The updated_dt of this OctoPrintSettings.  # noqa: E501
        :type updated_dt: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_dt is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_dt`, must not be `None`")  # noqa: E501

        self._updated_dt = updated_dt

    @property
    def octoprint_server(self):
        """Gets the octoprint_server of this OctoPrintSettings.  # noqa: E501


        :return: The octoprint_server of this OctoPrintSettings.  # noqa: E501
        :rtype: int
        """
        return self._octoprint_server

    @octoprint_server.setter
    def octoprint_server(self, octoprint_server):
        """Sets the octoprint_server of this OctoPrintSettings.


        :param octoprint_server: The octoprint_server of this OctoPrintSettings.  # noqa: E501
        :type octoprint_server: int
        """
        if self.local_vars_configuration.client_side_validation and octoprint_server is None:  # noqa: E501
            raise ValueError("Invalid value for `octoprint_server`, must not be `None`")  # noqa: E501

        self._octoprint_server = octoprint_server

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
        if not isinstance(other, OctoPrintSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OctoPrintSettings):
            return True

        return self.to_dict() != other.to_dict()
