# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import collaboration_entity_pb2 as collaboration__entity__pb2
import collaboration_pb2 as collaboration__pb2
import entity_pb2 as entity__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class NoteServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveThread = channel.unary_unary(
                '/calixa.domain.collaboration.NoteService/SaveThread',
                request_serializer=entity__pb2.SaveEntityRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.GetAssociatedThreads = channel.unary_stream(
                '/calixa.domain.collaboration.NoteService/GetAssociatedThreads',
                request_serializer=collaboration__pb2.GetAssociatedThreadsRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.SaveMessage = channel.unary_unary(
                '/calixa.domain.collaboration.NoteService/SaveMessage',
                request_serializer=entity__pb2.SaveEntityRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.GetMessages = channel.unary_stream(
                '/calixa.domain.collaboration.NoteService/GetMessages',
                request_serializer=collaboration__pb2.GetMessageRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.GetLatestMessage = channel.unary_unary(
                '/calixa.domain.collaboration.NoteService/GetLatestMessage',
                request_serializer=collaboration__pb2.ThreadReference.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.AddOrganizationUserNotification = channel.unary_unary(
                '/calixa.domain.collaboration.NoteService/AddOrganizationUserNotification',
                request_serializer=collaboration__pb2.OrganizationUserNotificationRequest.SerializeToString,
                response_deserializer=collaboration__entity__pb2.OrganizationUserNotification.FromString,
                )
        self.MarkNotificationRead = channel.unary_unary(
                '/calixa.domain.collaboration.NoteService/MarkNotificationRead',
                request_serializer=collaboration__pb2.NotificationReference.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetOrganizationUserNotifications = channel.unary_stream(
                '/calixa.domain.collaboration.NoteService/GetOrganizationUserNotifications',
                request_serializer=collaboration__pb2.GetOrganizationUserNotificationsRequest.SerializeToString,
                response_deserializer=collaboration__entity__pb2.OrganizationUserNotification.FromString,
                )
        self.GetThreadNotifications = channel.unary_stream(
                '/calixa.domain.collaboration.NoteService/GetThreadNotifications',
                request_serializer=collaboration__pb2.GetThreadNotificationsRequest.SerializeToString,
                response_deserializer=collaboration__entity__pb2.OrganizationUserNotification.FromString,
                )


class NoteServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SaveThread(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAssociatedThreads(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddOrganizationUserNotification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkNotificationRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOrganizationUserNotifications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetThreadNotifications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NoteServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaveThread': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveThread,
                    request_deserializer=entity__pb2.SaveEntityRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'GetAssociatedThreads': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAssociatedThreads,
                    request_deserializer=collaboration__pb2.GetAssociatedThreadsRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'SaveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveMessage,
                    request_deserializer=entity__pb2.SaveEntityRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'GetMessages': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMessages,
                    request_deserializer=collaboration__pb2.GetMessageRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'GetLatestMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLatestMessage,
                    request_deserializer=collaboration__pb2.ThreadReference.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'AddOrganizationUserNotification': grpc.unary_unary_rpc_method_handler(
                    servicer.AddOrganizationUserNotification,
                    request_deserializer=collaboration__pb2.OrganizationUserNotificationRequest.FromString,
                    response_serializer=collaboration__entity__pb2.OrganizationUserNotification.SerializeToString,
            ),
            'MarkNotificationRead': grpc.unary_unary_rpc_method_handler(
                    servicer.MarkNotificationRead,
                    request_deserializer=collaboration__pb2.NotificationReference.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetOrganizationUserNotifications': grpc.unary_stream_rpc_method_handler(
                    servicer.GetOrganizationUserNotifications,
                    request_deserializer=collaboration__pb2.GetOrganizationUserNotificationsRequest.FromString,
                    response_serializer=collaboration__entity__pb2.OrganizationUserNotification.SerializeToString,
            ),
            'GetThreadNotifications': grpc.unary_stream_rpc_method_handler(
                    servicer.GetThreadNotifications,
                    request_deserializer=collaboration__pb2.GetThreadNotificationsRequest.FromString,
                    response_serializer=collaboration__entity__pb2.OrganizationUserNotification.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'calixa.domain.collaboration.NoteService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NoteService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SaveThread(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.collaboration.NoteService/SaveThread',
            entity__pb2.SaveEntityRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAssociatedThreads(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.collaboration.NoteService/GetAssociatedThreads',
            collaboration__pb2.GetAssociatedThreadsRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.collaboration.NoteService/SaveMessage',
            entity__pb2.SaveEntityRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMessages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.collaboration.NoteService/GetMessages',
            collaboration__pb2.GetMessageRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLatestMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.collaboration.NoteService/GetLatestMessage',
            collaboration__pb2.ThreadReference.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddOrganizationUserNotification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.collaboration.NoteService/AddOrganizationUserNotification',
            collaboration__pb2.OrganizationUserNotificationRequest.SerializeToString,
            collaboration__entity__pb2.OrganizationUserNotification.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MarkNotificationRead(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.collaboration.NoteService/MarkNotificationRead',
            collaboration__pb2.NotificationReference.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOrganizationUserNotifications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.collaboration.NoteService/GetOrganizationUserNotifications',
            collaboration__pb2.GetOrganizationUserNotificationsRequest.SerializeToString,
            collaboration__entity__pb2.OrganizationUserNotification.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetThreadNotifications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.collaboration.NoteService/GetThreadNotifications',
            collaboration__pb2.GetThreadNotificationsRequest.SerializeToString,
            collaboration__entity__pb2.OrganizationUserNotification.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
