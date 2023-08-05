# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    NewType as typing___NewType,
    cast as typing___cast,
)


builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

IntegrationSourceValue = typing___NewType('IntegrationSourceValue', builtin___int)
type___IntegrationSourceValue = IntegrationSourceValue
IntegrationSource: _IntegrationSource
class _IntegrationSource(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[IntegrationSourceValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    INTEGRATION_SOURCE_UNSPECIFIED = typing___cast(IntegrationSourceValue, 0)
    INTEGRATION_SOURCE_STRIPE = typing___cast(IntegrationSourceValue, 1)
    INTEGRATION_SOURCE_MAILGUN = typing___cast(IntegrationSourceValue, 3)
    INTEGRATION_SOURCE_SEGMENT = typing___cast(IntegrationSourceValue, 4)
    INTEGRATION_SOURCE_ZENDESK = typing___cast(IntegrationSourceValue, 5)
    INTEGRATION_SOURCE_INTERCOM = typing___cast(IntegrationSourceValue, 6)
    INTEGRATION_SOURCE_FRONT = typing___cast(IntegrationSourceValue, 7)
    INTEGRATION_SOURCE_SENDGRID = typing___cast(IntegrationSourceValue, 8)
    INTEGRATION_SOURCE_FRESHDESK = typing___cast(IntegrationSourceValue, 9)
    INTEGRATION_SOURCE_SENTRY = typing___cast(IntegrationSourceValue, 10)
    INTEGRATION_SOURCE_SALESFORCE = typing___cast(IntegrationSourceValue, 11)
    INTEGRATION_SOURCE_HUBSPOT = typing___cast(IntegrationSourceValue, 12)
    INTEGRATION_SOURCE_GOOGLE_FIREBASE = typing___cast(IntegrationSourceValue, 13)
    INTEGRATION_SOURCE_SLACK = typing___cast(IntegrationSourceValue, 14)
    INTEGRATION_SOURCE_SALESLOFT = typing___cast(IntegrationSourceValue, 15)
    INTEGRATION_SOURCE_OUTREACH = typing___cast(IntegrationSourceValue, 16)
    INTEGRATION_SOURCE_CLEARBIT = typing___cast(IntegrationSourceValue, 17)
    INTEGRATION_SOURCE_AMPLITUDE = typing___cast(IntegrationSourceValue, 18)
    INTEGRATION_SOURCE_MIXPANEL = typing___cast(IntegrationSourceValue, 19)
    INTEGRATION_SOURCE_AUTO_METRICS = typing___cast(IntegrationSourceValue, 536870907)
    INTEGRATION_SOURCE_ORGANIZATION = typing___cast(IntegrationSourceValue, 536870908)
    INTEGRATION_SOURCE_UNIVERSAL_EMAIL = typing___cast(IntegrationSourceValue, 536870909)
    INTEGRATION_SOURCE_CALIXA_CONSOLE = typing___cast(IntegrationSourceValue, 536870910)
    INTEGRATION_SOURCE_CALIXA_API = typing___cast(IntegrationSourceValue, 536870911)
INTEGRATION_SOURCE_UNSPECIFIED = typing___cast(IntegrationSourceValue, 0)
INTEGRATION_SOURCE_STRIPE = typing___cast(IntegrationSourceValue, 1)
INTEGRATION_SOURCE_MAILGUN = typing___cast(IntegrationSourceValue, 3)
INTEGRATION_SOURCE_SEGMENT = typing___cast(IntegrationSourceValue, 4)
INTEGRATION_SOURCE_ZENDESK = typing___cast(IntegrationSourceValue, 5)
INTEGRATION_SOURCE_INTERCOM = typing___cast(IntegrationSourceValue, 6)
INTEGRATION_SOURCE_FRONT = typing___cast(IntegrationSourceValue, 7)
INTEGRATION_SOURCE_SENDGRID = typing___cast(IntegrationSourceValue, 8)
INTEGRATION_SOURCE_FRESHDESK = typing___cast(IntegrationSourceValue, 9)
INTEGRATION_SOURCE_SENTRY = typing___cast(IntegrationSourceValue, 10)
INTEGRATION_SOURCE_SALESFORCE = typing___cast(IntegrationSourceValue, 11)
INTEGRATION_SOURCE_HUBSPOT = typing___cast(IntegrationSourceValue, 12)
INTEGRATION_SOURCE_GOOGLE_FIREBASE = typing___cast(IntegrationSourceValue, 13)
INTEGRATION_SOURCE_SLACK = typing___cast(IntegrationSourceValue, 14)
INTEGRATION_SOURCE_SALESLOFT = typing___cast(IntegrationSourceValue, 15)
INTEGRATION_SOURCE_OUTREACH = typing___cast(IntegrationSourceValue, 16)
INTEGRATION_SOURCE_CLEARBIT = typing___cast(IntegrationSourceValue, 17)
INTEGRATION_SOURCE_AMPLITUDE = typing___cast(IntegrationSourceValue, 18)
INTEGRATION_SOURCE_MIXPANEL = typing___cast(IntegrationSourceValue, 19)
INTEGRATION_SOURCE_AUTO_METRICS = typing___cast(IntegrationSourceValue, 536870907)
INTEGRATION_SOURCE_ORGANIZATION = typing___cast(IntegrationSourceValue, 536870908)
INTEGRATION_SOURCE_UNIVERSAL_EMAIL = typing___cast(IntegrationSourceValue, 536870909)
INTEGRATION_SOURCE_CALIXA_CONSOLE = typing___cast(IntegrationSourceValue, 536870910)
INTEGRATION_SOURCE_CALIXA_API = typing___cast(IntegrationSourceValue, 536870911)
type___IntegrationSource = IntegrationSource

IntegrationStoreValue = typing___NewType('IntegrationStoreValue', builtin___int)
type___IntegrationStoreValue = IntegrationStoreValue
IntegrationStore: _IntegrationStore
class _IntegrationStore(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[IntegrationStoreValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    INTEGRATION_STORE_UNSPECIFIED = typing___cast(IntegrationStoreValue, 0)
    INTEGRATION_STORE_BIGQUERY = typing___cast(IntegrationStoreValue, 1)
    INTEGRATION_STORE_SNOWFLAKE = typing___cast(IntegrationStoreValue, 2)
    INTEGRATION_STORE_REDSHIFT = typing___cast(IntegrationStoreValue, 3)
INTEGRATION_STORE_UNSPECIFIED = typing___cast(IntegrationStoreValue, 0)
INTEGRATION_STORE_BIGQUERY = typing___cast(IntegrationStoreValue, 1)
INTEGRATION_STORE_SNOWFLAKE = typing___cast(IntegrationStoreValue, 2)
INTEGRATION_STORE_REDSHIFT = typing___cast(IntegrationStoreValue, 3)
type___IntegrationStore = IntegrationStore

IntegrationChannelValue = typing___NewType('IntegrationChannelValue', builtin___int)
type___IntegrationChannelValue = IntegrationChannelValue
IntegrationChannel: _IntegrationChannel
class _IntegrationChannel(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[IntegrationChannelValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    INTEGRATION_CHANNEL_UNSPECIFIED = typing___cast(IntegrationChannelValue, 0)
    INTEGRATION_CHANNEL_DIRECT = typing___cast(IntegrationChannelValue, 1)
    INTEGRATION_CHANNEL_AIRBYTE = typing___cast(IntegrationChannelValue, 3)
    INTEGRATION_CHANNEL_CENSUS = typing___cast(IntegrationChannelValue, 4)
    INTEGRATION_CHANNEL_INTERNAL = typing___cast(IntegrationChannelValue, 5)
INTEGRATION_CHANNEL_UNSPECIFIED = typing___cast(IntegrationChannelValue, 0)
INTEGRATION_CHANNEL_DIRECT = typing___cast(IntegrationChannelValue, 1)
INTEGRATION_CHANNEL_AIRBYTE = typing___cast(IntegrationChannelValue, 3)
INTEGRATION_CHANNEL_CENSUS = typing___cast(IntegrationChannelValue, 4)
INTEGRATION_CHANNEL_INTERNAL = typing___cast(IntegrationChannelValue, 5)
type___IntegrationChannel = IntegrationChannel
