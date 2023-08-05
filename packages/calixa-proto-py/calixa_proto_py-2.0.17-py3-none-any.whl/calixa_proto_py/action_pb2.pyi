# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from common_pb2 import (
    Amount as common_pb2___Amount,
    EntityTypeValue as common_pb2___EntityTypeValue,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.struct_pb2 import (
    Struct as google___protobuf___struct_pb2___Struct,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from integration_source_pb2 import (
    IntegrationSourceValue as integration_source_pb2___IntegrationSourceValue,
)

from typing import (
    Iterable as typing___Iterable,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

ActionStateValue = typing___NewType('ActionStateValue', builtin___int)
type___ActionStateValue = ActionStateValue
ActionState: _ActionState
class _ActionState(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[ActionStateValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    ACTION_STATE_UNSPECIFIED = typing___cast(ActionStateValue, 0)
    ACTION_STATE_ENABLED = typing___cast(ActionStateValue, 1)
    ACTION_STATE_DISABLED = typing___cast(ActionStateValue, 2)
ACTION_STATE_UNSPECIFIED = typing___cast(ActionStateValue, 0)
ACTION_STATE_ENABLED = typing___cast(ActionStateValue, 1)
ACTION_STATE_DISABLED = typing___cast(ActionStateValue, 2)
type___ActionState = ActionState

ActionInvocationStatusValue = typing___NewType('ActionInvocationStatusValue', builtin___int)
type___ActionInvocationStatusValue = ActionInvocationStatusValue
ActionInvocationStatus: _ActionInvocationStatus
class _ActionInvocationStatus(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[ActionInvocationStatusValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    ACTION_INVOCATION_STATUS_UNSPECIFIED = typing___cast(ActionInvocationStatusValue, 0)
    ACTION_INVOCATION_STATUS_SUCCESS = typing___cast(ActionInvocationStatusValue, 1)
    ACTION_INVOCATION_STATUS_FAILED = typing___cast(ActionInvocationStatusValue, 2)
ACTION_INVOCATION_STATUS_UNSPECIFIED = typing___cast(ActionInvocationStatusValue, 0)
ACTION_INVOCATION_STATUS_SUCCESS = typing___cast(ActionInvocationStatusValue, 1)
ACTION_INVOCATION_STATUS_FAILED = typing___cast(ActionInvocationStatusValue, 2)
type___ActionInvocationStatus = ActionInvocationStatus

AutomationActionFrequencyValue = typing___NewType('AutomationActionFrequencyValue', builtin___int)
type___AutomationActionFrequencyValue = AutomationActionFrequencyValue
AutomationActionFrequency: _AutomationActionFrequency
class _AutomationActionFrequency(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[AutomationActionFrequencyValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    AUTOMATION_FREQUENCY_UNSPECIFIED = typing___cast(AutomationActionFrequencyValue, 0)
    AUTOMATION_FREQUENCY_HOURLY = typing___cast(AutomationActionFrequencyValue, 1)
    AUTOMATION_FREQUENCY_DAILY = typing___cast(AutomationActionFrequencyValue, 2)
    AUTOMATION_FREQUENCY_WEEKLY = typing___cast(AutomationActionFrequencyValue, 3)
    AUTOMATION_FREQUENCY_MONTHLY = typing___cast(AutomationActionFrequencyValue, 4)
    AUTOMATION_FREQUENCY_QUARTERLY = typing___cast(AutomationActionFrequencyValue, 5)
    AUTOMATION_FREQUENCY_YEARLY = typing___cast(AutomationActionFrequencyValue, 6)
    AUTOMATION_FREQUENCY_ALL_TIME = typing___cast(AutomationActionFrequencyValue, 1000)
AUTOMATION_FREQUENCY_UNSPECIFIED = typing___cast(AutomationActionFrequencyValue, 0)
AUTOMATION_FREQUENCY_HOURLY = typing___cast(AutomationActionFrequencyValue, 1)
AUTOMATION_FREQUENCY_DAILY = typing___cast(AutomationActionFrequencyValue, 2)
AUTOMATION_FREQUENCY_WEEKLY = typing___cast(AutomationActionFrequencyValue, 3)
AUTOMATION_FREQUENCY_MONTHLY = typing___cast(AutomationActionFrequencyValue, 4)
AUTOMATION_FREQUENCY_QUARTERLY = typing___cast(AutomationActionFrequencyValue, 5)
AUTOMATION_FREQUENCY_YEARLY = typing___cast(AutomationActionFrequencyValue, 6)
AUTOMATION_FREQUENCY_ALL_TIME = typing___cast(AutomationActionFrequencyValue, 1000)
type___AutomationActionFrequency = AutomationActionFrequency

ActionTypeValue = typing___NewType('ActionTypeValue', builtin___int)
type___ActionTypeValue = ActionTypeValue
ActionType: _ActionType
class _ActionType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[ActionTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    ACTION_TYPE_UNSPECIFIED = typing___cast(ActionTypeValue, 0)
    ACTION_TYPE_CHARGE_REFUND = typing___cast(ActionTypeValue, 1)
    ACTION_TYPE_SUBSCRIPTION_TRIAL_UPDATE = typing___cast(ActionTypeValue, 100)
    ACTION_TYPE_COUPON_APPLY = typing___cast(ActionTypeValue, 200)
    ACTION_TYPE_OPPORTUNITY_CREATE = typing___cast(ActionTypeValue, 300)
    ACTION_TYPE_OPPORTUNITY_CREATE_USER = typing___cast(ActionTypeValue, 301)
    ACTION_TYPE_TASK_CREATE = typing___cast(ActionTypeValue, 400)
    ACTION_TYPE_TASK_CREATE_USER = typing___cast(ActionTypeValue, 401)
    ACTION_TYPE_CADENCE_ADD_PERSON = typing___cast(ActionTypeValue, 500)
    ACTION_TYPE_SEQUENCE_ADD_PROSPECT = typing___cast(ActionTypeValue, 600)
    ACTION_TYPE_CUSTOM = typing___cast(ActionTypeValue, 10000)
    ACTION_TYPE_REDIRECT = typing___cast(ActionTypeValue, 10001)
    ACTION_TYPE_ADD_TO_CONTACT_LIST = typing___cast(ActionTypeValue, 700)
    ACTION_TYPE_CREATE_LEAD = typing___cast(ActionTypeValue, 800)
ACTION_TYPE_UNSPECIFIED = typing___cast(ActionTypeValue, 0)
ACTION_TYPE_CHARGE_REFUND = typing___cast(ActionTypeValue, 1)
ACTION_TYPE_SUBSCRIPTION_TRIAL_UPDATE = typing___cast(ActionTypeValue, 100)
ACTION_TYPE_COUPON_APPLY = typing___cast(ActionTypeValue, 200)
ACTION_TYPE_OPPORTUNITY_CREATE = typing___cast(ActionTypeValue, 300)
ACTION_TYPE_OPPORTUNITY_CREATE_USER = typing___cast(ActionTypeValue, 301)
ACTION_TYPE_TASK_CREATE = typing___cast(ActionTypeValue, 400)
ACTION_TYPE_TASK_CREATE_USER = typing___cast(ActionTypeValue, 401)
ACTION_TYPE_CADENCE_ADD_PERSON = typing___cast(ActionTypeValue, 500)
ACTION_TYPE_SEQUENCE_ADD_PROSPECT = typing___cast(ActionTypeValue, 600)
ACTION_TYPE_CUSTOM = typing___cast(ActionTypeValue, 10000)
ACTION_TYPE_REDIRECT = typing___cast(ActionTypeValue, 10001)
ACTION_TYPE_ADD_TO_CONTACT_LIST = typing___cast(ActionTypeValue, 700)
ACTION_TYPE_CREATE_LEAD = typing___cast(ActionTypeValue, 800)
type___ActionType = ActionType

DisplayFieldTypeValue = typing___NewType('DisplayFieldTypeValue', builtin___int)
type___DisplayFieldTypeValue = DisplayFieldTypeValue
DisplayFieldType: _DisplayFieldType
class _DisplayFieldType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[DisplayFieldTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    DISPLAY_FIELD_TYPE_UNSPECIFIED = typing___cast(DisplayFieldTypeValue, 0)
    DISPLAY_FIELD_TYPE_AMOUNT = typing___cast(DisplayFieldTypeValue, 1)
    DISPLAY_FIELD_TYPE_BOOLEAN = typing___cast(DisplayFieldTypeValue, 2)
    DISPLAY_FIELD_TYPE_COUNTRY = typing___cast(DisplayFieldTypeValue, 3)
    DISPLAY_FIELD_TYPE_CURRENCY = typing___cast(DisplayFieldTypeValue, 4)
    DISPLAY_FIELD_TYPE_DATE = typing___cast(DisplayFieldTypeValue, 5)
    DISPLAY_FIELD_TYPE_ENUM = typing___cast(DisplayFieldTypeValue, 6)
    DISPLAY_FIELD_TYPE_MICROS = typing___cast(DisplayFieldTypeValue, 7)
    DISPLAY_FIELD_TYPE_NUMBER = typing___cast(DisplayFieldTypeValue, 8)
    DISPLAY_FIELD_TYPE_PERCENTAGE = typing___cast(DisplayFieldTypeValue, 9)
    DISPLAY_FIELD_TYPE_STRING = typing___cast(DisplayFieldTypeValue, 10)
    DISPLAY_FIELD_TYPE_RENDERABLE = typing___cast(DisplayFieldTypeValue, 11)
    DISPLAY_FIELD_TYPE_HIDDEN = typing___cast(DisplayFieldTypeValue, 12)
DISPLAY_FIELD_TYPE_UNSPECIFIED = typing___cast(DisplayFieldTypeValue, 0)
DISPLAY_FIELD_TYPE_AMOUNT = typing___cast(DisplayFieldTypeValue, 1)
DISPLAY_FIELD_TYPE_BOOLEAN = typing___cast(DisplayFieldTypeValue, 2)
DISPLAY_FIELD_TYPE_COUNTRY = typing___cast(DisplayFieldTypeValue, 3)
DISPLAY_FIELD_TYPE_CURRENCY = typing___cast(DisplayFieldTypeValue, 4)
DISPLAY_FIELD_TYPE_DATE = typing___cast(DisplayFieldTypeValue, 5)
DISPLAY_FIELD_TYPE_ENUM = typing___cast(DisplayFieldTypeValue, 6)
DISPLAY_FIELD_TYPE_MICROS = typing___cast(DisplayFieldTypeValue, 7)
DISPLAY_FIELD_TYPE_NUMBER = typing___cast(DisplayFieldTypeValue, 8)
DISPLAY_FIELD_TYPE_PERCENTAGE = typing___cast(DisplayFieldTypeValue, 9)
DISPLAY_FIELD_TYPE_STRING = typing___cast(DisplayFieldTypeValue, 10)
DISPLAY_FIELD_TYPE_RENDERABLE = typing___cast(DisplayFieldTypeValue, 11)
DISPLAY_FIELD_TYPE_HIDDEN = typing___cast(DisplayFieldTypeValue, 12)
type___DisplayFieldType = DisplayFieldType

DisplayFieldContextValue = typing___NewType('DisplayFieldContextValue', builtin___int)
type___DisplayFieldContextValue = DisplayFieldContextValue
DisplayFieldContext: _DisplayFieldContext
class _DisplayFieldContext(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[DisplayFieldContextValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    DISPLAY_FIELD_CONTEXT_UNSPECIFIED = typing___cast(DisplayFieldContextValue, 0)
    DISPLAY_FIELD_CONTEXT_ACTION = typing___cast(DisplayFieldContextValue, 1)
    DISPLAY_FIELD_CONTEXT_AUTOMATION = typing___cast(DisplayFieldContextValue, 2)
DISPLAY_FIELD_CONTEXT_UNSPECIFIED = typing___cast(DisplayFieldContextValue, 0)
DISPLAY_FIELD_CONTEXT_ACTION = typing___cast(DisplayFieldContextValue, 1)
DISPLAY_FIELD_CONTEXT_AUTOMATION = typing___cast(DisplayFieldContextValue, 2)
type___DisplayFieldContext = DisplayFieldContext

class ChargeRefundParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    reason: typing___Text = ...

    @property
    def amount(self) -> common_pb2___Amount: ...

    def __init__(self,
        *,
        amount : typing___Optional[common_pb2___Amount] = None,
        reason : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"amount",b"amount"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"amount",b"amount",u"reason",b"reason"]) -> None: ...
type___ChargeRefundParams = ChargeRefundParams

class SubscriptionTrialUpdateParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def trial_end_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        trial_end_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"trial_end_at",b"trial_end_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"trial_end_at",b"trial_end_at"]) -> None: ...
type___SubscriptionTrialUpdateParams = SubscriptionTrialUpdateParams

class CouponApplyParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    coupon_id: typing___Text = ...

    def __init__(self,
        *,
        coupon_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"coupon_id",b"coupon_id"]) -> None: ...
type___CouponApplyParams = CouponApplyParams

class OpportunityCreateParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...
    stage_name: typing___Text = ...
    owner_id: typing___Text = ...
    opportunity_type: typing___Text = ...
    account_id: typing___Text = ...
    contact_id: typing___Text = ...
    deal_pipeline: typing___Text = ...

    @property
    def closed_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def amount(self) -> common_pb2___Amount: ...

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        closed_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        amount : typing___Optional[common_pb2___Amount] = None,
        stage_name : typing___Optional[typing___Text] = None,
        owner_id : typing___Optional[typing___Text] = None,
        opportunity_type : typing___Optional[typing___Text] = None,
        account_id : typing___Optional[typing___Text] = None,
        contact_id : typing___Optional[typing___Text] = None,
        deal_pipeline : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"amount",b"amount",u"closed_at",b"closed_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_id",b"account_id",u"amount",b"amount",u"closed_at",b"closed_at",u"contact_id",b"contact_id",u"deal_pipeline",b"deal_pipeline",u"name",b"name",u"opportunity_type",b"opportunity_type",u"owner_id",b"owner_id",u"stage_name",b"stage_name"]) -> None: ...
type___OpportunityCreateParams = OpportunityCreateParams

class TaskCreateParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    owner_id: typing___Text = ...
    body: typing___Text = ...
    title: typing___Text = ...
    status: typing___Text = ...
    priority: typing___Text = ...
    account_id: typing___Text = ...
    contact_id: typing___Text = ...
    relative_days: builtin___int = ...

    @property
    def timestamp(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        owner_id : typing___Optional[typing___Text] = None,
        timestamp : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        body : typing___Optional[typing___Text] = None,
        title : typing___Optional[typing___Text] = None,
        status : typing___Optional[typing___Text] = None,
        priority : typing___Optional[typing___Text] = None,
        account_id : typing___Optional[typing___Text] = None,
        contact_id : typing___Optional[typing___Text] = None,
        relative_days : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"timestamp",b"timestamp"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_id",b"account_id",u"body",b"body",u"contact_id",b"contact_id",u"owner_id",b"owner_id",u"priority",b"priority",u"relative_days",b"relative_days",u"status",b"status",u"timestamp",b"timestamp",u"title",b"title"]) -> None: ...
type___TaskCreateParams = TaskCreateParams

class OwnershipUpdateParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    owner_id: typing___Text = ...
    owned_object_id: typing___Text = ...
    owned_object_type: common_pb2___EntityTypeValue = ...

    def __init__(self,
        *,
        owner_id : typing___Optional[typing___Text] = None,
        owned_object_id : typing___Optional[typing___Text] = None,
        owned_object_type : typing___Optional[common_pb2___EntityTypeValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"owned_object_id",b"owned_object_id",u"owned_object_type",b"owned_object_type",u"owner_id",b"owner_id"]) -> None: ...
type___OwnershipUpdateParams = OwnershipUpdateParams

class CadenceAddPersonParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    cadence_id: typing___Text = ...
    person_id: typing___Text = ...
    owner_id: typing___Text = ...
    user_id: typing___Text = ...
    owner_mailbox: typing___Text = ...

    def __init__(self,
        *,
        cadence_id : typing___Optional[typing___Text] = None,
        person_id : typing___Optional[typing___Text] = None,
        owner_id : typing___Optional[typing___Text] = None,
        user_id : typing___Optional[typing___Text] = None,
        owner_mailbox : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"cadence_id",b"cadence_id",u"owner_id",b"owner_id",u"owner_mailbox",b"owner_mailbox",u"person_id",b"person_id",u"user_id",b"user_id"]) -> None: ...
type___CadenceAddPersonParams = CadenceAddPersonParams

class SequenceAddProspectParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    sequence_id: typing___Text = ...
    prospect_id: typing___Text = ...
    mailbox_id: typing___Text = ...
    owner_email: typing___Text = ...

    def __init__(self,
        *,
        sequence_id : typing___Optional[typing___Text] = None,
        prospect_id : typing___Optional[typing___Text] = None,
        mailbox_id : typing___Optional[typing___Text] = None,
        owner_email : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"mailbox_id",b"mailbox_id",u"owner_email",b"owner_email",u"prospect_id",b"prospect_id",u"sequence_id",b"sequence_id"]) -> None: ...
type___SequenceAddProspectParams = SequenceAddProspectParams

class CustomParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def payload(self) -> google___protobuf___struct_pb2___Struct: ...

    def __init__(self,
        *,
        payload : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"payload",b"payload"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"payload",b"payload"]) -> None: ...
type___CustomParams = CustomParams

class RedirectParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    url: typing___Text = ...

    def __init__(self,
        *,
        url : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"url",b"url"]) -> None: ...
type___RedirectParams = RedirectParams

class AddToContactListParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    list_id: typing___Text = ...
    contact_id: typing___Text = ...

    def __init__(self,
        *,
        list_id : typing___Optional[typing___Text] = None,
        contact_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"contact_id",b"contact_id",u"list_id",b"list_id"]) -> None: ...
type___AddToContactListParams = AddToContactListParams

class LeadCreateParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    email: typing___Text = ...
    first_name: typing___Text = ...
    last_name: typing___Text = ...
    company_name: typing___Text = ...

    def __init__(self,
        *,
        email : typing___Optional[typing___Text] = None,
        first_name : typing___Optional[typing___Text] = None,
        last_name : typing___Optional[typing___Text] = None,
        company_name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"company_name",b"company_name",u"email",b"email",u"first_name",b"first_name",u"last_name",b"last_name"]) -> None: ...
type___LeadCreateParams = LeadCreateParams

class RequestConfig(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    url: typing___Text = ...
    httpMethod: typing___Text = ...
    headers: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...

    @property
    def payload(self) -> google___protobuf___struct_pb2___Struct: ...

    def __init__(self,
        *,
        url : typing___Optional[typing___Text] = None,
        httpMethod : typing___Optional[typing___Text] = None,
        headers : typing___Optional[typing___Iterable[typing___Text]] = None,
        payload : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"payload",b"payload"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"headers",b"headers",u"httpMethod",b"httpMethod",u"payload",b"payload",u"url",b"url"]) -> None: ...
type___RequestConfig = RequestConfig

class ActionParams(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def charge_refund_params(self) -> type___ChargeRefundParams: ...

    @property
    def subscription_trial_update_params(self) -> type___SubscriptionTrialUpdateParams: ...

    @property
    def coupon_apply_params(self) -> type___CouponApplyParams: ...

    @property
    def opportunity_create_params(self) -> type___OpportunityCreateParams: ...

    @property
    def task_create_params(self) -> type___TaskCreateParams: ...

    @property
    def cadence_add_person_params(self) -> type___CadenceAddPersonParams: ...

    @property
    def sequence_add_prospect_params(self) -> type___SequenceAddProspectParams: ...

    @property
    def ownership_update_params(self) -> type___OwnershipUpdateParams: ...

    @property
    def custom_params(self) -> type___CustomParams: ...

    @property
    def redirect_params(self) -> type___RedirectParams: ...

    @property
    def add_to_contact_list_params(self) -> type___AddToContactListParams: ...

    @property
    def lead_create_params(self) -> type___LeadCreateParams: ...

    def __init__(self,
        *,
        charge_refund_params : typing___Optional[type___ChargeRefundParams] = None,
        subscription_trial_update_params : typing___Optional[type___SubscriptionTrialUpdateParams] = None,
        coupon_apply_params : typing___Optional[type___CouponApplyParams] = None,
        opportunity_create_params : typing___Optional[type___OpportunityCreateParams] = None,
        task_create_params : typing___Optional[type___TaskCreateParams] = None,
        cadence_add_person_params : typing___Optional[type___CadenceAddPersonParams] = None,
        sequence_add_prospect_params : typing___Optional[type___SequenceAddProspectParams] = None,
        ownership_update_params : typing___Optional[type___OwnershipUpdateParams] = None,
        custom_params : typing___Optional[type___CustomParams] = None,
        redirect_params : typing___Optional[type___RedirectParams] = None,
        add_to_contact_list_params : typing___Optional[type___AddToContactListParams] = None,
        lead_create_params : typing___Optional[type___LeadCreateParams] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"add_to_contact_list_params",b"add_to_contact_list_params",u"cadence_add_person_params",b"cadence_add_person_params",u"charge_refund_params",b"charge_refund_params",u"coupon_apply_params",b"coupon_apply_params",u"custom_params",b"custom_params",u"lead_create_params",b"lead_create_params",u"opportunity_create_params",b"opportunity_create_params",u"ownership_update_params",b"ownership_update_params",u"params",b"params",u"redirect_params",b"redirect_params",u"sequence_add_prospect_params",b"sequence_add_prospect_params",u"subscription_trial_update_params",b"subscription_trial_update_params",u"task_create_params",b"task_create_params"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"add_to_contact_list_params",b"add_to_contact_list_params",u"cadence_add_person_params",b"cadence_add_person_params",u"charge_refund_params",b"charge_refund_params",u"coupon_apply_params",b"coupon_apply_params",u"custom_params",b"custom_params",u"lead_create_params",b"lead_create_params",u"opportunity_create_params",b"opportunity_create_params",u"ownership_update_params",b"ownership_update_params",u"params",b"params",u"redirect_params",b"redirect_params",u"sequence_add_prospect_params",b"sequence_add_prospect_params",u"subscription_trial_update_params",b"subscription_trial_update_params",u"task_create_params",b"task_create_params"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"params",b"params"]) -> typing_extensions___Literal["charge_refund_params","subscription_trial_update_params","coupon_apply_params","opportunity_create_params","task_create_params","cadence_add_person_params","sequence_add_prospect_params","ownership_update_params","custom_params","redirect_params","add_to_contact_list_params","lead_create_params"]: ...
type___ActionParams = ActionParams

class ThirdPartyActionInvocationResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class HeadersEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...
        value: typing___Text = ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___HeadersEntry = HeadersEntry

    class MetaEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...
        value: typing___Text = ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___MetaEntry = MetaEntry

    body: typing___Text = ...
    status_code: builtin___int = ...

    @property
    def headers(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    @property
    def meta(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    def __init__(self,
        *,
        headers : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        meta : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        body : typing___Optional[typing___Text] = None,
        status_code : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"body",b"body",u"headers",b"headers",u"meta",b"meta",u"status_code",b"status_code"]) -> None: ...
type___ThirdPartyActionInvocationResponse = ThirdPartyActionInvocationResponse

class ActionConfig(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    title: typing___Text = ...
    source: integration_source_pb2___IntegrationSourceValue = ...
    entity_type: common_pb2___EntityTypeValue = ...
    created_by_organization_user: typing___Text = ...
    action_state: type___ActionStateValue = ...
    action_type: type___ActionTypeValue = ...
    description: typing___Text = ...
    display_on_entity_types: google___protobuf___internal___containers___RepeatedScalarFieldContainer[common_pb2___EntityTypeValue] = ...
    installed_by_parent_integration: builtin___bool = ...

    @property
    def default_action_params(self) -> type___ActionParams: ...

    @property
    def request_config(self) -> type___RequestConfig: ...

    @property
    def display_fields(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___DisplayField]: ...

    def __init__(self,
        *,
        title : typing___Optional[typing___Text] = None,
        source : typing___Optional[integration_source_pb2___IntegrationSourceValue] = None,
        entity_type : typing___Optional[common_pb2___EntityTypeValue] = None,
        created_by_organization_user : typing___Optional[typing___Text] = None,
        default_action_params : typing___Optional[type___ActionParams] = None,
        action_state : typing___Optional[type___ActionStateValue] = None,
        action_type : typing___Optional[type___ActionTypeValue] = None,
        description : typing___Optional[typing___Text] = None,
        request_config : typing___Optional[type___RequestConfig] = None,
        display_fields : typing___Optional[typing___Iterable[type___DisplayField]] = None,
        display_on_entity_types : typing___Optional[typing___Iterable[common_pb2___EntityTypeValue]] = None,
        installed_by_parent_integration : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"default_action_params",b"default_action_params",u"request_config",b"request_config"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"action_state",b"action_state",u"action_type",b"action_type",u"created_by_organization_user",b"created_by_organization_user",u"default_action_params",b"default_action_params",u"description",b"description",u"display_fields",b"display_fields",u"display_on_entity_types",b"display_on_entity_types",u"entity_type",b"entity_type",u"installed_by_parent_integration",b"installed_by_parent_integration",u"request_config",b"request_config",u"source",b"source",u"title",b"title"]) -> None: ...
type___ActionConfig = ActionConfig

class DisplayField(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class InitialValueEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...
        value: typing___Text = ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___InitialValueEntry = InitialValueEntry

    class RenderWhenEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...
        value: typing___Text = ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___RenderWhenEntry = RenderWhenEntry

    key: typing___Text = ...
    display: typing___Text = ...
    field_type: type___DisplayFieldTypeValue = ...
    placeholder: typing___Text = ...
    required: builtin___bool = ...
    supplied_by_entity_type: common_pb2___EntityTypeValue = ...
    supplied_by_id_name: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...
    supplied_by_id_secondary_name: typing___Text = ...
    supplied_by_id_value: typing___Text = ...
    supplied_by_entity_filter: typing___Text = ...
    context: type___DisplayFieldContextValue = ...
    secondary_display: typing___Text = ...
    order: builtin___int = ...

    @property
    def options(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___Value]: ...

    @property
    def initial_value(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    @property
    def render_when(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    @property
    def properties(self) -> google___protobuf___struct_pb2___Struct: ...

    def __init__(self,
        *,
        key : typing___Optional[typing___Text] = None,
        display : typing___Optional[typing___Text] = None,
        field_type : typing___Optional[type___DisplayFieldTypeValue] = None,
        placeholder : typing___Optional[typing___Text] = None,
        required : typing___Optional[builtin___bool] = None,
        supplied_by_entity_type : typing___Optional[common_pb2___EntityTypeValue] = None,
        supplied_by_id_name : typing___Optional[typing___Iterable[typing___Text]] = None,
        supplied_by_id_secondary_name : typing___Optional[typing___Text] = None,
        supplied_by_id_value : typing___Optional[typing___Text] = None,
        supplied_by_entity_filter : typing___Optional[typing___Text] = None,
        context : typing___Optional[type___DisplayFieldContextValue] = None,
        secondary_display : typing___Optional[typing___Text] = None,
        options : typing___Optional[typing___Iterable[type___Value]] = None,
        initial_value : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        render_when : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        properties : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        order : typing___Optional[builtin___int] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"properties",b"properties"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"context",b"context",u"display",b"display",u"field_type",b"field_type",u"initial_value",b"initial_value",u"key",b"key",u"options",b"options",u"order",b"order",u"placeholder",b"placeholder",u"properties",b"properties",u"render_when",b"render_when",u"required",b"required",u"secondary_display",b"secondary_display",u"supplied_by_entity_filter",b"supplied_by_entity_filter",u"supplied_by_entity_type",b"supplied_by_entity_type",u"supplied_by_id_name",b"supplied_by_id_name",u"supplied_by_id_secondary_name",b"supplied_by_id_secondary_name",u"supplied_by_id_value",b"supplied_by_id_value"]) -> None: ...
type___DisplayField = DisplayField

class Value(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    key: typing___Text = ...
    display: typing___Text = ...

    def __init__(self,
        *,
        key : typing___Optional[typing___Text] = None,
        display : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"display",b"display",u"key",b"key"]) -> None: ...
type___Value = Value
