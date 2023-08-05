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


class NatsOrganization(object):
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
        'name': 'str',
        'is_active': 'bool',
        'created': 'datetime',
        'modified': 'datetime',
        'slug': 'str',
        'json': 'dict(str, object)',
        'imports': 'list[int]',
        'exports': 'list[int]',
        'users': 'list[int]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'is_active': 'is_active',
        'created': 'created',
        'modified': 'modified',
        'slug': 'slug',
        'json': 'json',
        'imports': 'imports',
        'exports': 'exports',
        'users': 'users'
    }

    def __init__(self, id=None, name=None, is_active=None, created=None, modified=None, slug=None, json=None, imports=None, exports=None, users=None, local_vars_configuration=None):  # noqa: E501
        """NatsOrganization - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._is_active = None
        self._created = None
        self._modified = None
        self._slug = None
        self._json = None
        self._imports = None
        self._exports = None
        self._users = None
        self.discriminator = None

        self.id = id
        self.name = name
        if is_active is not None:
            self.is_active = is_active
        self.created = created
        self.modified = modified
        self.slug = slug
        if json is not None:
            self.json = json
        self.imports = imports
        self.exports = exports
        self.users = users

    @property
    def id(self):
        """Gets the id of this NatsOrganization.  # noqa: E501


        :return: The id of this NatsOrganization.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this NatsOrganization.


        :param id: The id of this NatsOrganization.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this NatsOrganization.  # noqa: E501

        The name of the organization  # noqa: E501

        :return: The name of this NatsOrganization.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NatsOrganization.

        The name of the organization  # noqa: E501

        :param name: The name of this NatsOrganization.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 200):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `200`")  # noqa: E501

        self._name = name

    @property
    def is_active(self):
        """Gets the is_active of this NatsOrganization.  # noqa: E501


        :return: The is_active of this NatsOrganization.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this NatsOrganization.


        :param is_active: The is_active of this NatsOrganization.  # noqa: E501
        :type is_active: bool
        """

        self._is_active = is_active

    @property
    def created(self):
        """Gets the created of this NatsOrganization.  # noqa: E501


        :return: The created of this NatsOrganization.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this NatsOrganization.


        :param created: The created of this NatsOrganization.  # noqa: E501
        :type created: datetime
        """
        if self.local_vars_configuration.client_side_validation and created is None:  # noqa: E501
            raise ValueError("Invalid value for `created`, must not be `None`")  # noqa: E501

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this NatsOrganization.  # noqa: E501


        :return: The modified of this NatsOrganization.  # noqa: E501
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this NatsOrganization.


        :param modified: The modified of this NatsOrganization.  # noqa: E501
        :type modified: datetime
        """
        if self.local_vars_configuration.client_side_validation and modified is None:  # noqa: E501
            raise ValueError("Invalid value for `modified`, must not be `None`")  # noqa: E501

        self._modified = modified

    @property
    def slug(self):
        """Gets the slug of this NatsOrganization.  # noqa: E501

        The name in all lowercase, suitable for URL identification  # noqa: E501

        :return: The slug of this NatsOrganization.  # noqa: E501
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """Sets the slug of this NatsOrganization.

        The name in all lowercase, suitable for URL identification  # noqa: E501

        :param slug: The slug of this NatsOrganization.  # noqa: E501
        :type slug: str
        """
        if self.local_vars_configuration.client_side_validation and slug is None:  # noqa: E501
            raise ValueError("Invalid value for `slug`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and len(slug) > 200):
            raise ValueError("Invalid value for `slug`, length must be less than or equal to `200`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                slug is not None and not re.search(r'^[-a-zA-Z0-9_]+$', slug)):  # noqa: E501
            raise ValueError(r"Invalid value for `slug`, must be a follow pattern or equal to `/^[-a-zA-Z0-9_]+$/`")  # noqa: E501

        self._slug = slug

    @property
    def json(self):
        """Gets the json of this NatsOrganization.  # noqa: E501

        Output of `nsc describe account`  # noqa: E501

        :return: The json of this NatsOrganization.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._json

    @json.setter
    def json(self, json):
        """Sets the json of this NatsOrganization.

        Output of `nsc describe account`  # noqa: E501

        :param json: The json of this NatsOrganization.  # noqa: E501
        :type json: dict(str, object)
        """

        self._json = json

    @property
    def imports(self):
        """Gets the imports of this NatsOrganization.  # noqa: E501


        :return: The imports of this NatsOrganization.  # noqa: E501
        :rtype: list[int]
        """
        return self._imports

    @imports.setter
    def imports(self, imports):
        """Sets the imports of this NatsOrganization.


        :param imports: The imports of this NatsOrganization.  # noqa: E501
        :type imports: list[int]
        """
        if self.local_vars_configuration.client_side_validation and imports is None:  # noqa: E501
            raise ValueError("Invalid value for `imports`, must not be `None`")  # noqa: E501

        self._imports = imports

    @property
    def exports(self):
        """Gets the exports of this NatsOrganization.  # noqa: E501


        :return: The exports of this NatsOrganization.  # noqa: E501
        :rtype: list[int]
        """
        return self._exports

    @exports.setter
    def exports(self, exports):
        """Sets the exports of this NatsOrganization.


        :param exports: The exports of this NatsOrganization.  # noqa: E501
        :type exports: list[int]
        """
        if self.local_vars_configuration.client_side_validation and exports is None:  # noqa: E501
            raise ValueError("Invalid value for `exports`, must not be `None`")  # noqa: E501

        self._exports = exports

    @property
    def users(self):
        """Gets the users of this NatsOrganization.  # noqa: E501


        :return: The users of this NatsOrganization.  # noqa: E501
        :rtype: list[int]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this NatsOrganization.


        :param users: The users of this NatsOrganization.  # noqa: E501
        :type users: list[int]
        """
        if self.local_vars_configuration.client_side_validation and users is None:  # noqa: E501
            raise ValueError("Invalid value for `users`, must not be `None`")  # noqa: E501

        self._users = users

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
        if not isinstance(other, NatsOrganization):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NatsOrganization):
            return True

        return self.to_dict() != other.to_dict()
