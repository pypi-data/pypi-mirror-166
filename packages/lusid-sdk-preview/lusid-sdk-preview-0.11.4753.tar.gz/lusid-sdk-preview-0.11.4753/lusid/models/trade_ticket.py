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


class TradeTicket(object):
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
        'transaction_id': 'str',
        'type': 'str',
        'source': 'str',
        'transaction_date': 'str',
        'settlement_date': 'str',
        'total_consideration': 'CurrencyAndAmount',
        'units': 'float',
        'instrument_identifiers': 'dict(str, str)',
        'instrument_scope': 'str',
        'instrument_name': 'str',
        'instrument_definition': 'LusidInstrument',
        'counterparty_agreement_id': 'ResourceId'
    }

    attribute_map = {
        'transaction_id': 'transactionId',
        'type': 'type',
        'source': 'source',
        'transaction_date': 'transactionDate',
        'settlement_date': 'settlementDate',
        'total_consideration': 'totalConsideration',
        'units': 'units',
        'instrument_identifiers': 'instrumentIdentifiers',
        'instrument_scope': 'instrumentScope',
        'instrument_name': 'instrumentName',
        'instrument_definition': 'instrumentDefinition',
        'counterparty_agreement_id': 'counterpartyAgreementId'
    }

    required_map = {
        'transaction_id': 'required',
        'type': 'required',
        'source': 'optional',
        'transaction_date': 'required',
        'settlement_date': 'required',
        'total_consideration': 'required',
        'units': 'required',
        'instrument_identifiers': 'required',
        'instrument_scope': 'optional',
        'instrument_name': 'optional',
        'instrument_definition': 'optional',
        'counterparty_agreement_id': 'optional'
    }

    def __init__(self, transaction_id=None, type=None, source=None, transaction_date=None, settlement_date=None, total_consideration=None, units=None, instrument_identifiers=None, instrument_scope=None, instrument_name=None, instrument_definition=None, counterparty_agreement_id=None, local_vars_configuration=None):  # noqa: E501
        """TradeTicket - a model defined in OpenAPI"
        
        :param transaction_id:  The unique identifier of the transaction. (required)
        :type transaction_id: str
        :param type:  The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction. (required)
        :type type: str
        :param source:  The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.
        :type source: str
        :param transaction_date:  The date of the transaction. (required)
        :type transaction_date: str
        :param settlement_date:  The settlement date of the transaction. (required)
        :type settlement_date: str
        :param total_consideration:  (required)
        :type total_consideration: lusid.CurrencyAndAmount
        :param units:  The number of units of the transacted instrument. (required)
        :type units: float
        :param instrument_identifiers:  The set of identifiers that can be used to identify the instrument. (required)
        :type instrument_identifiers: dict(str, str)
        :param instrument_scope:  The scope in which the instrument lies.
        :type instrument_scope: str
        :param instrument_name:  The name of the instrument.
        :type instrument_name: str
        :param instrument_definition: 
        :type instrument_definition: lusid.LusidInstrument
        :param counterparty_agreement_id: 
        :type counterparty_agreement_id: lusid.ResourceId

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._transaction_id = None
        self._type = None
        self._source = None
        self._transaction_date = None
        self._settlement_date = None
        self._total_consideration = None
        self._units = None
        self._instrument_identifiers = None
        self._instrument_scope = None
        self._instrument_name = None
        self._instrument_definition = None
        self._counterparty_agreement_id = None
        self.discriminator = None

        self.transaction_id = transaction_id
        self.type = type
        self.source = source
        self.transaction_date = transaction_date
        self.settlement_date = settlement_date
        self.total_consideration = total_consideration
        self.units = units
        self.instrument_identifiers = instrument_identifiers
        self.instrument_scope = instrument_scope
        self.instrument_name = instrument_name
        if instrument_definition is not None:
            self.instrument_definition = instrument_definition
        if counterparty_agreement_id is not None:
            self.counterparty_agreement_id = counterparty_agreement_id

    @property
    def transaction_id(self):
        """Gets the transaction_id of this TradeTicket.  # noqa: E501

        The unique identifier of the transaction.  # noqa: E501

        :return: The transaction_id of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this TradeTicket.

        The unique identifier of the transaction.  # noqa: E501

        :param transaction_id: The transaction_id of this TradeTicket.  # noqa: E501
        :type transaction_id: str
        """
        if self.local_vars_configuration.client_side_validation and transaction_id is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                transaction_id is not None and len(transaction_id) > 256):
            raise ValueError("Invalid value for `transaction_id`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                transaction_id is not None and len(transaction_id) < 0):
            raise ValueError("Invalid value for `transaction_id`, length must be greater than or equal to `0`")  # noqa: E501

        self._transaction_id = transaction_id

    @property
    def type(self):
        """Gets the type of this TradeTicket.  # noqa: E501

        The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction.  # noqa: E501

        :return: The type of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TradeTicket.

        The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction.  # noqa: E501

        :param type: The type of this TradeTicket.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) > 256):
            raise ValueError("Invalid value for `type`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                type is not None and len(type) < 0):
            raise ValueError("Invalid value for `type`, length must be greater than or equal to `0`")  # noqa: E501

        self._type = type

    @property
    def source(self):
        """Gets the source of this TradeTicket.  # noqa: E501

        The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.  # noqa: E501

        :return: The source of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this TradeTicket.

        The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.  # noqa: E501

        :param source: The source of this TradeTicket.  # noqa: E501
        :type source: str
        """
        if (self.local_vars_configuration.client_side_validation and
                source is not None and len(source) > 256):
            raise ValueError("Invalid value for `source`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                source is not None and len(source) < 0):
            raise ValueError("Invalid value for `source`, length must be greater than or equal to `0`")  # noqa: E501

        self._source = source

    @property
    def transaction_date(self):
        """Gets the transaction_date of this TradeTicket.  # noqa: E501

        The date of the transaction.  # noqa: E501

        :return: The transaction_date of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        """Sets the transaction_date of this TradeTicket.

        The date of the transaction.  # noqa: E501

        :param transaction_date: The transaction_date of this TradeTicket.  # noqa: E501
        :type transaction_date: str
        """
        if self.local_vars_configuration.client_side_validation and transaction_date is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_date`, must not be `None`")  # noqa: E501

        self._transaction_date = transaction_date

    @property
    def settlement_date(self):
        """Gets the settlement_date of this TradeTicket.  # noqa: E501

        The settlement date of the transaction.  # noqa: E501

        :return: The settlement_date of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this TradeTicket.

        The settlement date of the transaction.  # noqa: E501

        :param settlement_date: The settlement_date of this TradeTicket.  # noqa: E501
        :type settlement_date: str
        """
        if self.local_vars_configuration.client_side_validation and settlement_date is None:  # noqa: E501
            raise ValueError("Invalid value for `settlement_date`, must not be `None`")  # noqa: E501

        self._settlement_date = settlement_date

    @property
    def total_consideration(self):
        """Gets the total_consideration of this TradeTicket.  # noqa: E501


        :return: The total_consideration of this TradeTicket.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._total_consideration

    @total_consideration.setter
    def total_consideration(self, total_consideration):
        """Sets the total_consideration of this TradeTicket.


        :param total_consideration: The total_consideration of this TradeTicket.  # noqa: E501
        :type total_consideration: lusid.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and total_consideration is None:  # noqa: E501
            raise ValueError("Invalid value for `total_consideration`, must not be `None`")  # noqa: E501

        self._total_consideration = total_consideration

    @property
    def units(self):
        """Gets the units of this TradeTicket.  # noqa: E501

        The number of units of the transacted instrument.  # noqa: E501

        :return: The units of this TradeTicket.  # noqa: E501
        :rtype: float
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this TradeTicket.

        The number of units of the transacted instrument.  # noqa: E501

        :param units: The units of this TradeTicket.  # noqa: E501
        :type units: float
        """
        if self.local_vars_configuration.client_side_validation and units is None:  # noqa: E501
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def instrument_identifiers(self):
        """Gets the instrument_identifiers of this TradeTicket.  # noqa: E501

        The set of identifiers that can be used to identify the instrument.  # noqa: E501

        :return: The instrument_identifiers of this TradeTicket.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._instrument_identifiers

    @instrument_identifiers.setter
    def instrument_identifiers(self, instrument_identifiers):
        """Sets the instrument_identifiers of this TradeTicket.

        The set of identifiers that can be used to identify the instrument.  # noqa: E501

        :param instrument_identifiers: The instrument_identifiers of this TradeTicket.  # noqa: E501
        :type instrument_identifiers: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and instrument_identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_identifiers`, must not be `None`")  # noqa: E501

        self._instrument_identifiers = instrument_identifiers

    @property
    def instrument_scope(self):
        """Gets the instrument_scope of this TradeTicket.  # noqa: E501

        The scope in which the instrument lies.  # noqa: E501

        :return: The instrument_scope of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._instrument_scope

    @instrument_scope.setter
    def instrument_scope(self, instrument_scope):
        """Sets the instrument_scope of this TradeTicket.

        The scope in which the instrument lies.  # noqa: E501

        :param instrument_scope: The instrument_scope of this TradeTicket.  # noqa: E501
        :type instrument_scope: str
        """
        if (self.local_vars_configuration.client_side_validation and
                instrument_scope is not None and len(instrument_scope) > 64):
            raise ValueError("Invalid value for `instrument_scope`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                instrument_scope is not None and len(instrument_scope) < 1):
            raise ValueError("Invalid value for `instrument_scope`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                instrument_scope is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', instrument_scope)):  # noqa: E501
            raise ValueError(r"Invalid value for `instrument_scope`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._instrument_scope = instrument_scope

    @property
    def instrument_name(self):
        """Gets the instrument_name of this TradeTicket.  # noqa: E501

        The name of the instrument.  # noqa: E501

        :return: The instrument_name of this TradeTicket.  # noqa: E501
        :rtype: str
        """
        return self._instrument_name

    @instrument_name.setter
    def instrument_name(self, instrument_name):
        """Sets the instrument_name of this TradeTicket.

        The name of the instrument.  # noqa: E501

        :param instrument_name: The instrument_name of this TradeTicket.  # noqa: E501
        :type instrument_name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                instrument_name is not None and len(instrument_name) > 256):
            raise ValueError("Invalid value for `instrument_name`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                instrument_name is not None and len(instrument_name) < 0):
            raise ValueError("Invalid value for `instrument_name`, length must be greater than or equal to `0`")  # noqa: E501

        self._instrument_name = instrument_name

    @property
    def instrument_definition(self):
        """Gets the instrument_definition of this TradeTicket.  # noqa: E501


        :return: The instrument_definition of this TradeTicket.  # noqa: E501
        :rtype: lusid.LusidInstrument
        """
        return self._instrument_definition

    @instrument_definition.setter
    def instrument_definition(self, instrument_definition):
        """Sets the instrument_definition of this TradeTicket.


        :param instrument_definition: The instrument_definition of this TradeTicket.  # noqa: E501
        :type instrument_definition: lusid.LusidInstrument
        """

        self._instrument_definition = instrument_definition

    @property
    def counterparty_agreement_id(self):
        """Gets the counterparty_agreement_id of this TradeTicket.  # noqa: E501


        :return: The counterparty_agreement_id of this TradeTicket.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._counterparty_agreement_id

    @counterparty_agreement_id.setter
    def counterparty_agreement_id(self, counterparty_agreement_id):
        """Sets the counterparty_agreement_id of this TradeTicket.


        :param counterparty_agreement_id: The counterparty_agreement_id of this TradeTicket.  # noqa: E501
        :type counterparty_agreement_id: lusid.ResourceId
        """

        self._counterparty_agreement_id = counterparty_agreement_id

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
        if not isinstance(other, TradeTicket):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TradeTicket):
            return True

        return self.to_dict() != other.to_dict()
