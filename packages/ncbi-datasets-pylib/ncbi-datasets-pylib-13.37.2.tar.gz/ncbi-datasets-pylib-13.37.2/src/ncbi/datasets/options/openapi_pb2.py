# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/options/openapi.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#ncbi/datasets/options/openapi.proto\x12\x15ncbi.datasets.options\x1a google/protobuf/descriptor.proto\"?\n\x15OpenApiRequestExample\x12&\n\x0f\x65xample_as_yaml\x18\x01 \x01(\tR\rexampleAsYaml\".\n\x12OpenApiFrontMatter\x12\x18\n\x07version\x18\x01 \x01(\tR\x07version\"9\n\x07\x45xample\x12\x14\n\x05value\x18\x01 \x03(\tR\x05value\x12\x18\n\x07summary\x18\x02 \x01(\tR\x07summary\"\x9e\x01\n\x13OpenapiFieldOptions\x12\x18\n\x07\x64\x65\x66\x61ult\x18\x01 \x01(\tR\x07\x64\x65\x66\x61ult\x12:\n\x08\x65xamples\x18\x02 \x03(\x0b\x32\x1e.ncbi.datasets.options.ExampleR\x08\x65xamples\x12\x31\n\x14report_specification\x18\x03 \x01(\tR\x13reportSpecification\"\xe4\x06\n\x16H1GatewayMethodOptions\x12T\n\tendpoints\x18\x01 \x03(\x0b\x32\x36.ncbi.datasets.options.H1GatewayMethodOptions.EndpointR\tendpoints\x1a\xb0\x05\n\x08\x45ndpoint\x12L\n\x06method\x18\x01 \x01(\x0e\x32\x34.ncbi.datasets.options.H1GatewayMethodOptions.MethodR\x06method\x12\x1f\n\x0b\x63urrent_url\x18\x02 \x01(\tR\ncurrentUrl\x12#\n\rprevious_urls\x18\x03 \x03(\tR\x0cpreviousUrls\x12\x1f\n\x0bhidden_urls\x18\x04 \x03(\tR\nhiddenUrls\x12\x18\n\x07summary\x18\x05 \x01(\tR\x07summary\x12 \n\x0b\x64\x65scription\x18\x06 \x01(\tR\x0b\x64\x65scription\x12!\n\x0coperation_id\x18\x07 \x01(\tR\x0boperationId\x12\x12\n\x04tags\x18\x08 \x03(\tR\x04tags\x12!\n\x0c\x65lide_params\x18\t \x03(\tR\x0b\x65lideParams\x12m\n\rrename_params\x18\n \x03(\x0b\x32H.ncbi.datasets.options.H1GatewayMethodOptions.Endpoint.RenameParamsEntryR\x0crenameParams\x12-\n\x12produces_jsonlines\x18\x0b \x01(\tR\x11producesJsonlines\x12\x1d\n\nomits_json\x18\x0c \x01(\x08R\tomitsJson\x12)\n\x10produces_tabular\x18\r \x01(\x08R\x0fproducesTabular\x12\x30\n\x14\x63ustom_accept_header\x18\x0e \x03(\tR\x12\x63ustomAcceptHeader\x1a?\n\x11RenameParamsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"A\n\x06Method\x12\x16\n\x12METHOD_UNSPECIFIED\x10\x00\x12\x0e\n\nMETHOD_GET\x10\x01\x12\x0f\n\x0bMETHOD_POST\x10\x02:{\n\x14openapi_front_matter\x12\x1c.google.protobuf.FileOptions\x18\x88\x9e\x03 \x01(\x0b\x32).ncbi.datasets.options.OpenApiFrontMatterR\x12openapiFrontMatter:e\n\x07openapi\x12\x1d.google.protobuf.FieldOptions\x18\x88\x9e\x03 \x01(\x0b\x32*.ncbi.datasets.options.OpenapiFieldOptionsR\x07openapi:i\n\x07gateway\x12\x1e.google.protobuf.MethodOptions\x18\x88\x9e\x03 \x01(\x0b\x32-.ncbi.datasets.options.H1GatewayMethodOptionsR\x07gateway:x\n\x0frequest_example\x12\x1f.google.protobuf.MessageOptions\x18\x88\x9e\x03 \x01(\x0b\x32,.ncbi.datasets.options.OpenApiRequestExampleR\x0erequestExampleB\x1aZ\x15ncbi/datasets/options\xf8\x01\x01\x62\x06proto3')


OPENAPI_FRONT_MATTER_FIELD_NUMBER = 53000
openapi_front_matter = DESCRIPTOR.extensions_by_name['openapi_front_matter']
OPENAPI_FIELD_NUMBER = 53000
openapi = DESCRIPTOR.extensions_by_name['openapi']
GATEWAY_FIELD_NUMBER = 53000
gateway = DESCRIPTOR.extensions_by_name['gateway']
REQUEST_EXAMPLE_FIELD_NUMBER = 53000
request_example = DESCRIPTOR.extensions_by_name['request_example']

_OPENAPIREQUESTEXAMPLE = DESCRIPTOR.message_types_by_name['OpenApiRequestExample']
_OPENAPIFRONTMATTER = DESCRIPTOR.message_types_by_name['OpenApiFrontMatter']
_EXAMPLE = DESCRIPTOR.message_types_by_name['Example']
_OPENAPIFIELDOPTIONS = DESCRIPTOR.message_types_by_name['OpenapiFieldOptions']
_H1GATEWAYMETHODOPTIONS = DESCRIPTOR.message_types_by_name['H1GatewayMethodOptions']
_H1GATEWAYMETHODOPTIONS_ENDPOINT = _H1GATEWAYMETHODOPTIONS.nested_types_by_name['Endpoint']
_H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY = _H1GATEWAYMETHODOPTIONS_ENDPOINT.nested_types_by_name['RenameParamsEntry']
_H1GATEWAYMETHODOPTIONS_METHOD = _H1GATEWAYMETHODOPTIONS.enum_types_by_name['Method']
OpenApiRequestExample = _reflection.GeneratedProtocolMessageType('OpenApiRequestExample', (_message.Message,), {
  'DESCRIPTOR' : _OPENAPIREQUESTEXAMPLE,
  '__module__' : 'ncbi.datasets.options.openapi_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.options.OpenApiRequestExample)
  })
_sym_db.RegisterMessage(OpenApiRequestExample)

OpenApiFrontMatter = _reflection.GeneratedProtocolMessageType('OpenApiFrontMatter', (_message.Message,), {
  'DESCRIPTOR' : _OPENAPIFRONTMATTER,
  '__module__' : 'ncbi.datasets.options.openapi_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.options.OpenApiFrontMatter)
  })
_sym_db.RegisterMessage(OpenApiFrontMatter)

Example = _reflection.GeneratedProtocolMessageType('Example', (_message.Message,), {
  'DESCRIPTOR' : _EXAMPLE,
  '__module__' : 'ncbi.datasets.options.openapi_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.options.Example)
  })
_sym_db.RegisterMessage(Example)

OpenapiFieldOptions = _reflection.GeneratedProtocolMessageType('OpenapiFieldOptions', (_message.Message,), {
  'DESCRIPTOR' : _OPENAPIFIELDOPTIONS,
  '__module__' : 'ncbi.datasets.options.openapi_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.options.OpenapiFieldOptions)
  })
_sym_db.RegisterMessage(OpenapiFieldOptions)

H1GatewayMethodOptions = _reflection.GeneratedProtocolMessageType('H1GatewayMethodOptions', (_message.Message,), {

  'Endpoint' : _reflection.GeneratedProtocolMessageType('Endpoint', (_message.Message,), {

    'RenameParamsEntry' : _reflection.GeneratedProtocolMessageType('RenameParamsEntry', (_message.Message,), {
      'DESCRIPTOR' : _H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY,
      '__module__' : 'ncbi.datasets.options.openapi_pb2'
      # @@protoc_insertion_point(class_scope:ncbi.datasets.options.H1GatewayMethodOptions.Endpoint.RenameParamsEntry)
      })
    ,
    'DESCRIPTOR' : _H1GATEWAYMETHODOPTIONS_ENDPOINT,
    '__module__' : 'ncbi.datasets.options.openapi_pb2'
    # @@protoc_insertion_point(class_scope:ncbi.datasets.options.H1GatewayMethodOptions.Endpoint)
    })
  ,
  'DESCRIPTOR' : _H1GATEWAYMETHODOPTIONS,
  '__module__' : 'ncbi.datasets.options.openapi_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.options.H1GatewayMethodOptions)
  })
_sym_db.RegisterMessage(H1GatewayMethodOptions)
_sym_db.RegisterMessage(H1GatewayMethodOptions.Endpoint)
_sym_db.RegisterMessage(H1GatewayMethodOptions.Endpoint.RenameParamsEntry)

if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(openapi_front_matter)
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(openapi)
  google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(gateway)
  google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(request_example)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\025ncbi/datasets/options\370\001\001'
  _H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY._options = None
  _H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY._serialized_options = b'8\001'
  _OPENAPIREQUESTEXAMPLE._serialized_start=96
  _OPENAPIREQUESTEXAMPLE._serialized_end=159
  _OPENAPIFRONTMATTER._serialized_start=161
  _OPENAPIFRONTMATTER._serialized_end=207
  _EXAMPLE._serialized_start=209
  _EXAMPLE._serialized_end=266
  _OPENAPIFIELDOPTIONS._serialized_start=269
  _OPENAPIFIELDOPTIONS._serialized_end=427
  _H1GATEWAYMETHODOPTIONS._serialized_start=430
  _H1GATEWAYMETHODOPTIONS._serialized_end=1298
  _H1GATEWAYMETHODOPTIONS_ENDPOINT._serialized_start=543
  _H1GATEWAYMETHODOPTIONS_ENDPOINT._serialized_end=1231
  _H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY._serialized_start=1168
  _H1GATEWAYMETHODOPTIONS_ENDPOINT_RENAMEPARAMSENTRY._serialized_end=1231
  _H1GATEWAYMETHODOPTIONS_METHOD._serialized_start=1233
  _H1GATEWAYMETHODOPTIONS_METHOD._serialized_end=1298
# @@protoc_insertion_point(module_scope)
