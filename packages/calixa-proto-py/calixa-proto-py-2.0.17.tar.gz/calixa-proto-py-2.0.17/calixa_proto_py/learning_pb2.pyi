# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from common_pb2 import (
    EntityTypeValue as common_pb2___EntityTypeValue,
)

from entity_reference_pb2 import (
    EntityReference as entity_reference_pb2___EntityReference,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.duration_pb2 import (
    Duration as google___protobuf___duration_pb2___Duration,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.struct_pb2 import (
    Value as google___protobuf___struct_pb2___Value,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
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

FeatureValueTypeValue = typing___NewType('FeatureValueTypeValue', builtin___int)
type___FeatureValueTypeValue = FeatureValueTypeValue
FeatureValueType: _FeatureValueType
class _FeatureValueType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[FeatureValueTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    FEATURE_VALUE_TYPE_UNSPECIFIED = typing___cast(FeatureValueTypeValue, 0)
    FEATURE_VALUE_TYPE_INT64 = typing___cast(FeatureValueTypeValue, 1)
    FEATURE_VALUE_TYPE_DOUBLE = typing___cast(FeatureValueTypeValue, 2)
    FEATURE_VALUE_TYPE_STRING = typing___cast(FeatureValueTypeValue, 3)
    FEATURE_VALUE_TYPE_TIMESTAMP = typing___cast(FeatureValueTypeValue, 4)
    FEATURE_VALUE_TYPE_BOOLEAN = typing___cast(FeatureValueTypeValue, 5)
FEATURE_VALUE_TYPE_UNSPECIFIED = typing___cast(FeatureValueTypeValue, 0)
FEATURE_VALUE_TYPE_INT64 = typing___cast(FeatureValueTypeValue, 1)
FEATURE_VALUE_TYPE_DOUBLE = typing___cast(FeatureValueTypeValue, 2)
FEATURE_VALUE_TYPE_STRING = typing___cast(FeatureValueTypeValue, 3)
FEATURE_VALUE_TYPE_TIMESTAMP = typing___cast(FeatureValueTypeValue, 4)
FEATURE_VALUE_TYPE_BOOLEAN = typing___cast(FeatureValueTypeValue, 5)
type___FeatureValueType = FeatureValueType

PredictionTaskValue = typing___NewType('PredictionTaskValue', builtin___int)
type___PredictionTaskValue = PredictionTaskValue
PredictionTask: _PredictionTask
class _PredictionTask(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[PredictionTaskValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    PREDICTION_TASK_UNSPECIFIED = typing___cast(PredictionTaskValue, 0)
    PREDICTION_TASK_BIG_FISH = typing___cast(PredictionTaskValue, 1)
    PREDICTION_TASK_SAME_FISH = typing___cast(PredictionTaskValue, 2)
PREDICTION_TASK_UNSPECIFIED = typing___cast(PredictionTaskValue, 0)
PREDICTION_TASK_BIG_FISH = typing___cast(PredictionTaskValue, 1)
PREDICTION_TASK_SAME_FISH = typing___cast(PredictionTaskValue, 2)
type___PredictionTask = PredictionTask

ModelTypeValue = typing___NewType('ModelTypeValue', builtin___int)
type___ModelTypeValue = ModelTypeValue
ModelType: _ModelType
class _ModelType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[ModelTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    MODEL_TYPE_UNSPECIFIED = typing___cast(ModelTypeValue, 0)
    MODEL_TYPE_LOGISTIC_REG = typing___cast(ModelTypeValue, 1)
    MODEL_TYPE_KMEANS = typing___cast(ModelTypeValue, 2)
MODEL_TYPE_UNSPECIFIED = typing___cast(ModelTypeValue, 0)
MODEL_TYPE_LOGISTIC_REG = typing___cast(ModelTypeValue, 1)
MODEL_TYPE_KMEANS = typing___cast(ModelTypeValue, 2)
type___ModelType = ModelType

TaskLabelSourceValue = typing___NewType('TaskLabelSourceValue', builtin___int)
type___TaskLabelSourceValue = TaskLabelSourceValue
TaskLabelSource: _TaskLabelSource
class _TaskLabelSource(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[TaskLabelSourceValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    TASK_LABEL_SOURCE_UNSPECIFIED = typing___cast(TaskLabelSourceValue, 0)
    TASK_LABEL_SOURCE_AUTOMATIC = typing___cast(TaskLabelSourceValue, 1)
    TASK_LABEL_SOURCE_USER = typing___cast(TaskLabelSourceValue, 2)
TASK_LABEL_SOURCE_UNSPECIFIED = typing___cast(TaskLabelSourceValue, 0)
TASK_LABEL_SOURCE_AUTOMATIC = typing___cast(TaskLabelSourceValue, 1)
TASK_LABEL_SOURCE_USER = typing___cast(TaskLabelSourceValue, 2)
type___TaskLabelSource = TaskLabelSource

WorkflowStageValue = typing___NewType('WorkflowStageValue', builtin___int)
type___WorkflowStageValue = WorkflowStageValue
WorkflowStage: _WorkflowStage
class _WorkflowStage(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[WorkflowStageValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    WORKFLOW_STAGE_UNKNOWN = typing___cast(WorkflowStageValue, 0)
    WORKFLOW_STAGE_START = typing___cast(WorkflowStageValue, 1)
    WORKFLOW_STAGE_FEATURES = typing___cast(WorkflowStageValue, 2)
    WORKFLOW_STAGE_MODEL_TRAINING = typing___cast(WorkflowStageValue, 3)
    WORKFLOW_STAGE_PREDICTION = typing___cast(WorkflowStageValue, 4)
WORKFLOW_STAGE_UNKNOWN = typing___cast(WorkflowStageValue, 0)
WORKFLOW_STAGE_START = typing___cast(WorkflowStageValue, 1)
WORKFLOW_STAGE_FEATURES = typing___cast(WorkflowStageValue, 2)
WORKFLOW_STAGE_MODEL_TRAINING = typing___cast(WorkflowStageValue, 3)
WORKFLOW_STAGE_PREDICTION = typing___cast(WorkflowStageValue, 4)
type___WorkflowStage = WorkflowStage

JobTypeValue = typing___NewType('JobTypeValue', builtin___int)
type___JobTypeValue = JobTypeValue
JobType: _JobType
class _JobType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[JobTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    JOB_TYPE_UNKNOWN = typing___cast(JobTypeValue, 0)
    JOB_TYPE_BIG_QUERY = typing___cast(JobTypeValue, 1)
    JOB_TYPE_BEAM = typing___cast(JobTypeValue, 2)
JOB_TYPE_UNKNOWN = typing___cast(JobTypeValue, 0)
JOB_TYPE_BIG_QUERY = typing___cast(JobTypeValue, 1)
JOB_TYPE_BEAM = typing___cast(JobTypeValue, 2)
type___JobType = JobType

class FeatureDefinition(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    id: typing___Text = ...
    description: typing___Text = ...
    learnable: builtin___bool = ...
    type: type___FeatureValueTypeValue = ...

    def __init__(self,
        *,
        id : typing___Optional[typing___Text] = None,
        description : typing___Optional[typing___Text] = None,
        learnable : typing___Optional[builtin___bool] = None,
        type : typing___Optional[type___FeatureValueTypeValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"description",b"description",u"id",b"id",u"learnable",b"learnable",u"type",b"type"]) -> None: ...
type___FeatureDefinition = FeatureDefinition

class FeatureValue(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    feature_id: typing___Text = ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def value(self) -> google___protobuf___struct_pb2___Value: ...

    def __init__(self,
        *,
        feature_id : typing___Optional[typing___Text] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        value : typing___Optional[google___protobuf___struct_pb2___Value] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"value",b"value"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"feature_id",b"feature_id",u"value",b"value"]) -> None: ...
type___FeatureValue = FeatureValue

class PredictionTaskDefinition(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    prediction_id: typing___Text = ...
    prediction_task: type___PredictionTaskValue = ...
    entity_type: common_pb2___EntityTypeValue = ...

    @property
    def model_definitions(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___ModelDefinition]: ...

    def __init__(self,
        *,
        prediction_id : typing___Optional[typing___Text] = None,
        prediction_task : typing___Optional[type___PredictionTaskValue] = None,
        model_definitions : typing___Optional[typing___Iterable[type___ModelDefinition]] = None,
        entity_type : typing___Optional[common_pb2___EntityTypeValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"entity_type",b"entity_type",u"model_definitions",b"model_definitions",u"prediction_id",b"prediction_id",u"prediction_task",b"prediction_task"]) -> None: ...
type___PredictionTaskDefinition = PredictionTaskDefinition

class ModelDefinition(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    model_type: type___ModelTypeValue = ...

    @property
    def features(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___FeatureDefinition]: ...

    @property
    def rebuild_period(self) -> google___protobuf___duration_pb2___Duration: ...

    def __init__(self,
        *,
        model_type : typing___Optional[type___ModelTypeValue] = None,
        features : typing___Optional[typing___Iterable[type___FeatureDefinition]] = None,
        rebuild_period : typing___Optional[google___protobuf___duration_pb2___Duration] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"rebuild_period",b"rebuild_period"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"features",b"features",u"model_type",b"model_type",u"rebuild_period",b"rebuild_period"]) -> None: ...
type___ModelDefinition = ModelDefinition

class TaskLabel(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    prediction_task: type___PredictionTaskValue = ...
    label_source: type___TaskLabelSourceValue = ...

    @property
    def label(self) -> google___protobuf___struct_pb2___Value: ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        prediction_task : typing___Optional[type___PredictionTaskValue] = None,
        label_source : typing___Optional[type___TaskLabelSourceValue] = None,
        label : typing___Optional[google___protobuf___struct_pb2___Value] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"label",b"label"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"label",b"label",u"label_source",b"label_source",u"prediction_task",b"prediction_task"]) -> None: ...
type___TaskLabel = TaskLabel

class TaskModelPrediction(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class TopFeatureAttributionsEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key: typing___Text = ...
        value: builtin___float = ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[builtin___float] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    type___TopFeatureAttributionsEntry = TopFeatureAttributionsEntry

    prediction_task: type___PredictionTaskValue = ...
    model_type: type___ModelTypeValue = ...
    probability: builtin___float = ...

    @property
    def label(self) -> google___protobuf___struct_pb2___Value: ...

    @property
    def predicted_label(self) -> google___protobuf___struct_pb2___Value: ...

    @property
    def top_feature_attributions(self) -> typing___MutableMapping[typing___Text, builtin___float]: ...

    def __init__(self,
        *,
        prediction_task : typing___Optional[type___PredictionTaskValue] = None,
        model_type : typing___Optional[type___ModelTypeValue] = None,
        label : typing___Optional[google___protobuf___struct_pb2___Value] = None,
        predicted_label : typing___Optional[google___protobuf___struct_pb2___Value] = None,
        probability : typing___Optional[builtin___float] = None,
        top_feature_attributions : typing___Optional[typing___Mapping[typing___Text, builtin___float]] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"label",b"label",u"predicted_label",b"predicted_label"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"label",b"label",u"model_type",b"model_type",u"predicted_label",b"predicted_label",u"prediction_task",b"prediction_task",u"probability",b"probability",u"top_feature_attributions",b"top_feature_attributions"]) -> None: ...
type___TaskModelPrediction = TaskModelPrediction

class FeatureVector(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def entity_reference(self) -> entity_reference_pb2___EntityReference: ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def task_label(self) -> type___TaskLabel: ...

    @property
    def feature_values(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___FeatureValue]: ...

    def __init__(self,
        *,
        entity_reference : typing___Optional[entity_reference_pb2___EntityReference] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        task_label : typing___Optional[type___TaskLabel] = None,
        feature_values : typing___Optional[typing___Iterable[type___FeatureValue]] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"entity_reference",b"entity_reference",u"task_label",b"task_label"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"entity_reference",b"entity_reference",u"feature_values",b"feature_values",u"task_label",b"task_label"]) -> None: ...
type___FeatureVector = FeatureVector

class PredictionWorkflow(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    stage: type___WorkflowStageValue = ...
    organization_id: typing___Text = ...
    force_model_update: builtin___bool = ...

    @property
    def started_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def jobs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___PredictionJobId]: ...

    def __init__(self,
        *,
        stage : typing___Optional[type___WorkflowStageValue] = None,
        organization_id : typing___Optional[typing___Text] = None,
        started_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        jobs : typing___Optional[typing___Iterable[type___PredictionJobId]] = None,
        force_model_update : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"started_at",b"started_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"force_model_update",b"force_model_update",u"jobs",b"jobs",u"organization_id",b"organization_id",u"stage",b"stage",u"started_at",b"started_at"]) -> None: ...
type___PredictionWorkflow = PredictionWorkflow

class PredictionJobId(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    job_id: typing___Text = ...
    model_type: type___ModelTypeValue = ...
    prediction_task: type___PredictionTaskValue = ...
    location: typing___Text = ...
    project: typing___Text = ...
    job_type: type___JobTypeValue = ...

    def __init__(self,
        *,
        job_id : typing___Optional[typing___Text] = None,
        model_type : typing___Optional[type___ModelTypeValue] = None,
        prediction_task : typing___Optional[type___PredictionTaskValue] = None,
        location : typing___Optional[typing___Text] = None,
        project : typing___Optional[typing___Text] = None,
        job_type : typing___Optional[type___JobTypeValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"job_id",b"job_id",u"job_type",b"job_type",u"location",b"location",u"model_type",b"model_type",u"prediction_task",b"prediction_task",u"project",b"project"]) -> None: ...
type___PredictionJobId = PredictionJobId
