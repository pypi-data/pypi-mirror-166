# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: conversation.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import common_pb2 as common__pb2
import integration_source_pb2 as integration__source__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='conversation.proto',
  package='calixa.domain.conversation',
  syntax='proto3',
  serialized_options=b'\n\035io.calixa.domain.conversationH\001P\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12\x63onversation.proto\x12\x1a\x63\x61lixa.domain.conversation\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0c\x63ommon.proto\x1a\x18integration_source.proto\"A\n\x08UserLite\x12\x18\n\x10\x65xternal_user_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\"\x95\x02\n\x0c\x43onversation\x12!\n\x19\x65xternal_conversation_url\x18\x06 \x01(\t\x12\x0f\n\x07subject\x18\x07 \x01(\t\x12\x15\n\rmessage_count\x18\n \x01(\x03\x12\x34\n\x06\x61uthor\x18\x0b \x01(\x0b\x32$.calixa.domain.conversation.UserLite\x12:\n\x0cparticipants\x18\x0c \x03(\x0b\x32$.calixa.domain.conversation.UserLiteJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x06\x08\xf4\x03\x10\xf5\x03J\x06\x08\xf5\x03\x10\xf6\x03J\x06\x08\xfe\x03\x10\xff\x03J\x06\x08\xff\x03\x10\x80\x04\"\xbd\x04\n\x07Message\x12\x17\n\x0f\x63onversation_id\x18\x03 \x01(\t\x12\x16\n\x0e\x61uthor_user_id\x18\x04 \x01(\t\x12\x13\n\x0b\x61uthor_name\x18\x0b \x01(\t\x12\x14\n\x0c\x61uthor_email\x18\x0c \x01(\t\x12\x41\n\nvisibility\x18\x05 \x01(\x0e\x32-.calixa.domain.conversation.MessageVisibility\x12G\n\x11message_direction\x18\x08 \x01(\x0e\x32,.calixa.domain.conversation.MessageDirection\x12\x0c\n\x04\x62ody\x18\x06 \x01(\t\x12\x41\n\x0emessage_source\x18\x07 \x01(\x0e\x32).calixa.domain.conversation.MessageSource\x12\x1c\n\x14\x65xternal_message_url\x18\n \x01(\t\x12\x31\n\x03tos\x18\r \x03(\x0b\x32$.calixa.domain.conversation.UserLite\x12\x31\n\x03\x63\x63s\x18\x0e \x03(\x0b\x32$.calixa.domain.conversation.UserLite\x12=\n\x0cmessage_type\x18\x11 \x01(\x0e\x32\'.calixa.domain.conversation.MessageTypeJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x0f\x10\x10J\x04\x08\x10\x10\x11J\x06\x08\xf4\x03\x10\xf5\x03J\x06\x08\xf5\x03\x10\xf6\x03J\x06\x08\xfe\x03\x10\xff\x03J\x06\x08\xff\x03\x10\x80\x04\"\xbd\x01\n\nAttachment\x12\x17\n\x0f\x63onversation_id\x18\x03 \x01(\t\x12\x12\n\nmessage_id\x18\x04 \x01(\t\x12\x0b\n\x03url\x18\x05 \x01(\t\x12\x14\n\x0coriginal_url\x18\x06 \x01(\t\x12\x11\n\tfile_name\x18\x07 \x01(\t\x12\x14\n\x0c\x63ontent_type\x18\x08 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\t\x10\nJ\x04\x08\n\x10\x0bJ\x06\x08\xf4\x03\x10\xf5\x03J\x06\x08\xf5\x03\x10\xf6\x03J\x06\x08\xfe\x03\x10\xff\x03J\x06\x08\xff\x03\x10\x80\x04*\x99\x01\n\rMessageSource\x12\x1e\n\x1aMESSAGE_SOURCE_UNSPECIFIED\x10\x00\x12\x1a\n\x16MESSAGE_SOURCE_WEBFORM\x10\x01\x12\x1a\n\x16MESSAGE_SOURCE_WEBCHAT\x10\x02\x12\x18\n\x14MESSAGE_SOURCE_EMAIL\x10\x03\x12\x16\n\x12MESSAGE_SOURCE_SMS\x10\x04*w\n\x11MessageVisibility\x12\"\n\x1eMESSAGE_VISIBILITY_UNSPECIFIED\x10\x00\x12\x1d\n\x19MESSAGE_VISIBILITY_PUBLIC\x10\x01\x12\x1f\n\x1bMESSAGE_VISIBILITY_INTERNAL\x10\x02*t\n\x10MessageDirection\x12!\n\x1dMESSAGE_DIRECTION_UNSPECIFIED\x10\x00\x12\x1d\n\x19MESSAGE_DIRECTION_INBOUND\x10\x01\x12\x1e\n\x1aMESSAGE_DIRECTION_OUTBOUND\x10\x02*\xc0\x02\n\x0bMessageType\x12\x1c\n\x18MESSAGE_TYPE_UNSPECIFIED\x10\x00\x12\x15\n\x11MESSAGE_TYPE_CALL\x10\x01\x12\x17\n\x13MESSAGE_TYPE_CUSTOM\x10\x02\x12\x16\n\x12MESSAGE_TYPE_EMAIL\x10\x03\x12\x19\n\x15MESSAGE_TYPE_FACEBOOK\x10\x04\x12\x19\n\x15MESSAGE_TYPE_INTERCOM\x10\x05\x12\x17\n\x13MESSAGE_TYPE_SMOOCH\x10\x06\x12\x14\n\x10MESSAGE_TYPE_SMS\x10\x07\x12\x16\n\x12MESSAGE_TYPE_TWEET\x10\x08\x12\x19\n\x15MESSAGE_TYPE_TWEET_DM\x10\t\x12\x19\n\x15MESSAGE_TYPE_WHATSAPP\x10\n\x12\x18\n\x14MESSAGE_TYPE_ZENDESK\x10\x0b\x42#\n\x1dio.calixa.domain.conversationH\x01P\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,common__pb2.DESCRIPTOR,integration__source__pb2.DESCRIPTOR,])

_MESSAGESOURCE = _descriptor.EnumDescriptor(
  name='MessageSource',
  full_name='calixa.domain.conversation.MessageSource',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SOURCE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SOURCE_WEBFORM', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SOURCE_WEBCHAT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SOURCE_EMAIL', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SOURCE_SMS', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1273,
  serialized_end=1426,
)
_sym_db.RegisterEnumDescriptor(_MESSAGESOURCE)

MessageSource = enum_type_wrapper.EnumTypeWrapper(_MESSAGESOURCE)
_MESSAGEVISIBILITY = _descriptor.EnumDescriptor(
  name='MessageVisibility',
  full_name='calixa.domain.conversation.MessageVisibility',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_VISIBILITY_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_VISIBILITY_PUBLIC', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_VISIBILITY_INTERNAL', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1428,
  serialized_end=1547,
)
_sym_db.RegisterEnumDescriptor(_MESSAGEVISIBILITY)

MessageVisibility = enum_type_wrapper.EnumTypeWrapper(_MESSAGEVISIBILITY)
_MESSAGEDIRECTION = _descriptor.EnumDescriptor(
  name='MessageDirection',
  full_name='calixa.domain.conversation.MessageDirection',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_DIRECTION_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_DIRECTION_INBOUND', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_DIRECTION_OUTBOUND', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1549,
  serialized_end=1665,
)
_sym_db.RegisterEnumDescriptor(_MESSAGEDIRECTION)

MessageDirection = enum_type_wrapper.EnumTypeWrapper(_MESSAGEDIRECTION)
_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='calixa.domain.conversation.MessageType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_CALL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_CUSTOM', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_EMAIL', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_FACEBOOK', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_INTERCOM', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_SMOOCH', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_SMS', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_TWEET', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_TWEET_DM', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_WHATSAPP', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_TYPE_ZENDESK', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1668,
  serialized_end=1988,
)
_sym_db.RegisterEnumDescriptor(_MESSAGETYPE)

MessageType = enum_type_wrapper.EnumTypeWrapper(_MESSAGETYPE)
MESSAGE_SOURCE_UNSPECIFIED = 0
MESSAGE_SOURCE_WEBFORM = 1
MESSAGE_SOURCE_WEBCHAT = 2
MESSAGE_SOURCE_EMAIL = 3
MESSAGE_SOURCE_SMS = 4
MESSAGE_VISIBILITY_UNSPECIFIED = 0
MESSAGE_VISIBILITY_PUBLIC = 1
MESSAGE_VISIBILITY_INTERNAL = 2
MESSAGE_DIRECTION_UNSPECIFIED = 0
MESSAGE_DIRECTION_INBOUND = 1
MESSAGE_DIRECTION_OUTBOUND = 2
MESSAGE_TYPE_UNSPECIFIED = 0
MESSAGE_TYPE_CALL = 1
MESSAGE_TYPE_CUSTOM = 2
MESSAGE_TYPE_EMAIL = 3
MESSAGE_TYPE_FACEBOOK = 4
MESSAGE_TYPE_INTERCOM = 5
MESSAGE_TYPE_SMOOCH = 6
MESSAGE_TYPE_SMS = 7
MESSAGE_TYPE_TWEET = 8
MESSAGE_TYPE_TWEET_DM = 9
MESSAGE_TYPE_WHATSAPP = 10
MESSAGE_TYPE_ZENDESK = 11



_USERLITE = _descriptor.Descriptor(
  name='UserLite',
  full_name='calixa.domain.conversation.UserLite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='external_user_id', full_name='calixa.domain.conversation.UserLite.external_user_id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='calixa.domain.conversation.UserLite.name', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='calixa.domain.conversation.UserLite.email', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=222,
)


_CONVERSATION = _descriptor.Descriptor(
  name='Conversation',
  full_name='calixa.domain.conversation.Conversation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='external_conversation_url', full_name='calixa.domain.conversation.Conversation.external_conversation_url', index=0,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='subject', full_name='calixa.domain.conversation.Conversation.subject', index=1,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_count', full_name='calixa.domain.conversation.Conversation.message_count', index=2,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author', full_name='calixa.domain.conversation.Conversation.author', index=3,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='participants', full_name='calixa.domain.conversation.Conversation.participants', index=4,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=225,
  serialized_end=502,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='calixa.domain.conversation.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='conversation_id', full_name='calixa.domain.conversation.Message.conversation_id', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_user_id', full_name='calixa.domain.conversation.Message.author_user_id', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_name', full_name='calixa.domain.conversation.Message.author_name', index=2,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='author_email', full_name='calixa.domain.conversation.Message.author_email', index=3,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='visibility', full_name='calixa.domain.conversation.Message.visibility', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_direction', full_name='calixa.domain.conversation.Message.message_direction', index=5,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='calixa.domain.conversation.Message.body', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_source', full_name='calixa.domain.conversation.Message.message_source', index=7,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='external_message_url', full_name='calixa.domain.conversation.Message.external_message_url', index=8,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tos', full_name='calixa.domain.conversation.Message.tos', index=9,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ccs', full_name='calixa.domain.conversation.Message.ccs', index=10,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_type', full_name='calixa.domain.conversation.Message.message_type', index=11,
      number=17, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=505,
  serialized_end=1078,
)


_ATTACHMENT = _descriptor.Descriptor(
  name='Attachment',
  full_name='calixa.domain.conversation.Attachment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='conversation_id', full_name='calixa.domain.conversation.Attachment.conversation_id', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_id', full_name='calixa.domain.conversation.Attachment.message_id', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='calixa.domain.conversation.Attachment.url', index=2,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='original_url', full_name='calixa.domain.conversation.Attachment.original_url', index=3,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_name', full_name='calixa.domain.conversation.Attachment.file_name', index=4,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content_type', full_name='calixa.domain.conversation.Attachment.content_type', index=5,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1081,
  serialized_end=1270,
)

_CONVERSATION.fields_by_name['author'].message_type = _USERLITE
_CONVERSATION.fields_by_name['participants'].message_type = _USERLITE
_MESSAGE.fields_by_name['visibility'].enum_type = _MESSAGEVISIBILITY
_MESSAGE.fields_by_name['message_direction'].enum_type = _MESSAGEDIRECTION
_MESSAGE.fields_by_name['message_source'].enum_type = _MESSAGESOURCE
_MESSAGE.fields_by_name['tos'].message_type = _USERLITE
_MESSAGE.fields_by_name['ccs'].message_type = _USERLITE
_MESSAGE.fields_by_name['message_type'].enum_type = _MESSAGETYPE
DESCRIPTOR.message_types_by_name['UserLite'] = _USERLITE
DESCRIPTOR.message_types_by_name['Conversation'] = _CONVERSATION
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['Attachment'] = _ATTACHMENT
DESCRIPTOR.enum_types_by_name['MessageSource'] = _MESSAGESOURCE
DESCRIPTOR.enum_types_by_name['MessageVisibility'] = _MESSAGEVISIBILITY
DESCRIPTOR.enum_types_by_name['MessageDirection'] = _MESSAGEDIRECTION
DESCRIPTOR.enum_types_by_name['MessageType'] = _MESSAGETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserLite = _reflection.GeneratedProtocolMessageType('UserLite', (_message.Message,), {
  'DESCRIPTOR' : _USERLITE,
  '__module__' : 'conversation_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.conversation.UserLite)
  })
_sym_db.RegisterMessage(UserLite)

Conversation = _reflection.GeneratedProtocolMessageType('Conversation', (_message.Message,), {
  'DESCRIPTOR' : _CONVERSATION,
  '__module__' : 'conversation_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.conversation.Conversation)
  })
_sym_db.RegisterMessage(Conversation)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'conversation_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.conversation.Message)
  })
_sym_db.RegisterMessage(Message)

Attachment = _reflection.GeneratedProtocolMessageType('Attachment', (_message.Message,), {
  'DESCRIPTOR' : _ATTACHMENT,
  '__module__' : 'conversation_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.conversation.Attachment)
  })
_sym_db.RegisterMessage(Attachment)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
