# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.4753
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class VirtualDocument(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'document_id': 'StructuredResultDataId',
        'data': 'list[VirtualDocumentRow]'
    }

    attribute_map = {
        'document_id': 'documentId',
        'data': 'data'
    }

    required_map = {
        'document_id': 'optional',
        'data': 'optional'
    }

    def __init__(self, document_id=None, data=None, local_vars_configuration=None):  # noqa: E501
        """VirtualDocument - a model defined in OpenAPI"
        
        :param document_id: 
        :type document_id: lusid.StructuredResultDataId
        :param data:  The data inside the document
        :type data: list[lusid.VirtualDocumentRow]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._document_id = None
        self._data = None
        self.discriminator = None

        if document_id is not None:
            self.document_id = document_id
        self.data = data

    @property
    def document_id(self):
        """Gets the document_id of this VirtualDocument.  # noqa: E501


        :return: The document_id of this VirtualDocument.  # noqa: E501
        :rtype: lusid.StructuredResultDataId
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """Sets the document_id of this VirtualDocument.


        :param document_id: The document_id of this VirtualDocument.  # noqa: E501
        :type document_id: lusid.StructuredResultDataId
        """

        self._document_id = document_id

    @property
    def data(self):
        """Gets the data of this VirtualDocument.  # noqa: E501

        The data inside the document  # noqa: E501

        :return: The data of this VirtualDocument.  # noqa: E501
        :rtype: list[lusid.VirtualDocumentRow]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this VirtualDocument.

        The data inside the document  # noqa: E501

        :param data: The data of this VirtualDocument.  # noqa: E501
        :type data: list[lusid.VirtualDocumentRow]
        """

        self._data = data

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
        if not isinstance(other, VirtualDocument):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VirtualDocument):
            return True

        return self.to_dict() != other.to_dict()
