# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import metric_pb2 as metric__pb2


class MetricServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateMetricDescriptor = channel.unary_unary(
                '/calixa.domain.metric.MetricService/CreateMetricDescriptor',
                request_serializer=metric__pb2.CreateMetricDescriptorRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.GetMetricDescriptor = channel.unary_unary(
                '/calixa.domain.metric.MetricService/GetMetricDescriptor',
                request_serializer=metric__pb2.GetMetricDescriptorRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.FindOrCreateAutoMetricDescriptor = channel.unary_unary(
                '/calixa.domain.metric.MetricService/FindOrCreateAutoMetricDescriptor',
                request_serializer=metric__pb2.FindOrCreateAutoMetricDescriptorRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.GetMetricDescriptors = channel.unary_stream(
                '/calixa.domain.metric.MetricService/GetMetricDescriptors',
                request_serializer=metric__pb2.GetMetricDescriptorRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.UpdateMetricDescriptor = channel.unary_unary(
                '/calixa.domain.metric.MetricService/UpdateMetricDescriptor',
                request_serializer=metric__pb2.UpdateMetricDescriptorRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.GetMetricDescriptorsByPropertyKeyValue = channel.unary_stream(
                '/calixa.domain.metric.MetricService/GetMetricDescriptorsByPropertyKeyValue',
                request_serializer=metric__pb2.GetMetricDescriptorsByPropertyKeyValueRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricDescriptor.FromString,
                )
        self.GetTimeSeries = channel.unary_stream(
                '/calixa.domain.metric.MetricService/GetTimeSeries',
                request_serializer=metric__pb2.MetricTimeSeriesRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricObservationAtTime.FromString,
                )
        self.GetMetricSummary = channel.unary_unary(
                '/calixa.domain.metric.MetricService/GetMetricSummary',
                request_serializer=metric__pb2.MetricSummaryRequest.SerializeToString,
                response_deserializer=metric__pb2.MetricSummaryResponse.FromString,
                )
        self.GetEntitiesForConditions = channel.unary_unary(
                '/calixa.domain.metric.MetricService/GetEntitiesForConditions',
                request_serializer=metric__pb2.EntitiesForConditionsRequest.SerializeToString,
                response_deserializer=metric__pb2.EntitiesForConditionsResponse.FromString,
                )


class MetricServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateMetricDescriptor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetricDescriptor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindOrCreateAutoMetricDescriptor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetricDescriptors(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMetricDescriptor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetricDescriptorsByPropertyKeyValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTimeSeries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetricSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntitiesForConditions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MetricServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateMetricDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateMetricDescriptor,
                    request_deserializer=metric__pb2.CreateMetricDescriptorRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'GetMetricDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetricDescriptor,
                    request_deserializer=metric__pb2.GetMetricDescriptorRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'FindOrCreateAutoMetricDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.FindOrCreateAutoMetricDescriptor,
                    request_deserializer=metric__pb2.FindOrCreateAutoMetricDescriptorRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'GetMetricDescriptors': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMetricDescriptors,
                    request_deserializer=metric__pb2.GetMetricDescriptorRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'UpdateMetricDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateMetricDescriptor,
                    request_deserializer=metric__pb2.UpdateMetricDescriptorRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'GetMetricDescriptorsByPropertyKeyValue': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMetricDescriptorsByPropertyKeyValue,
                    request_deserializer=metric__pb2.GetMetricDescriptorsByPropertyKeyValueRequest.FromString,
                    response_serializer=metric__pb2.MetricDescriptor.SerializeToString,
            ),
            'GetTimeSeries': grpc.unary_stream_rpc_method_handler(
                    servicer.GetTimeSeries,
                    request_deserializer=metric__pb2.MetricTimeSeriesRequest.FromString,
                    response_serializer=metric__pb2.MetricObservationAtTime.SerializeToString,
            ),
            'GetMetricSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetricSummary,
                    request_deserializer=metric__pb2.MetricSummaryRequest.FromString,
                    response_serializer=metric__pb2.MetricSummaryResponse.SerializeToString,
            ),
            'GetEntitiesForConditions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntitiesForConditions,
                    request_deserializer=metric__pb2.EntitiesForConditionsRequest.FromString,
                    response_serializer=metric__pb2.EntitiesForConditionsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'calixa.domain.metric.MetricService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MetricService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateMetricDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/CreateMetricDescriptor',
            metric__pb2.CreateMetricDescriptorRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetricDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/GetMetricDescriptor',
            metric__pb2.GetMetricDescriptorRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindOrCreateAutoMetricDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/FindOrCreateAutoMetricDescriptor',
            metric__pb2.FindOrCreateAutoMetricDescriptorRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetricDescriptors(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.metric.MetricService/GetMetricDescriptors',
            metric__pb2.GetMetricDescriptorRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateMetricDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/UpdateMetricDescriptor',
            metric__pb2.UpdateMetricDescriptorRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetricDescriptorsByPropertyKeyValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.metric.MetricService/GetMetricDescriptorsByPropertyKeyValue',
            metric__pb2.GetMetricDescriptorsByPropertyKeyValueRequest.SerializeToString,
            metric__pb2.MetricDescriptor.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTimeSeries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.metric.MetricService/GetTimeSeries',
            metric__pb2.MetricTimeSeriesRequest.SerializeToString,
            metric__pb2.MetricObservationAtTime.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetricSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/GetMetricSummary',
            metric__pb2.MetricSummaryRequest.SerializeToString,
            metric__pb2.MetricSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntitiesForConditions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.metric.MetricService/GetEntitiesForConditions',
            metric__pb2.EntitiesForConditionsRequest.SerializeToString,
            metric__pb2.EntitiesForConditionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
