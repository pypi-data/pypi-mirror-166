/* This file was generated by upbc (the upb compiler) from the input
 * file:
 *
 *     envoy/api/v2/discovery.proto
 *
 * Do not edit -- your changes will be discarded when the file is
 * regenerated. */

#ifndef ENVOY_API_V2_DISCOVERY_PROTO_UPB_H_
#define ENVOY_API_V2_DISCOVERY_PROTO_UPB_H_

#include "upb/generated_util.h"
#include "upb/msg.h"
#include "upb/decode.h"
#include "upb/encode.h"

#include "upb/port_def.inc"

#ifdef __cplusplus
extern "C" {
#endif

struct envoy_api_v2_DiscoveryRequest;
struct envoy_api_v2_DiscoveryResponse;
struct envoy_api_v2_DeltaDiscoveryRequest;
struct envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry;
struct envoy_api_v2_DeltaDiscoveryResponse;
struct envoy_api_v2_Resource;
typedef struct envoy_api_v2_DiscoveryRequest envoy_api_v2_DiscoveryRequest;
typedef struct envoy_api_v2_DiscoveryResponse envoy_api_v2_DiscoveryResponse;
typedef struct envoy_api_v2_DeltaDiscoveryRequest envoy_api_v2_DeltaDiscoveryRequest;
typedef struct envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry;
typedef struct envoy_api_v2_DeltaDiscoveryResponse envoy_api_v2_DeltaDiscoveryResponse;
typedef struct envoy_api_v2_Resource envoy_api_v2_Resource;
extern const upb_msglayout envoy_api_v2_DiscoveryRequest_msginit;
extern const upb_msglayout envoy_api_v2_DiscoveryResponse_msginit;
extern const upb_msglayout envoy_api_v2_DeltaDiscoveryRequest_msginit;
extern const upb_msglayout envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_msginit;
extern const upb_msglayout envoy_api_v2_DeltaDiscoveryResponse_msginit;
extern const upb_msglayout envoy_api_v2_Resource_msginit;
struct envoy_api_v2_core_ControlPlane;
struct envoy_api_v2_core_Node;
struct google_protobuf_Any;
struct google_rpc_Status;
extern const upb_msglayout envoy_api_v2_core_ControlPlane_msginit;
extern const upb_msglayout envoy_api_v2_core_Node_msginit;
extern const upb_msglayout google_protobuf_Any_msginit;
extern const upb_msglayout google_rpc_Status_msginit;


/* envoy.api.v2.DiscoveryRequest */

UPB_INLINE envoy_api_v2_DiscoveryRequest *envoy_api_v2_DiscoveryRequest_new(upb_arena *arena) {
  return (envoy_api_v2_DiscoveryRequest *)upb_msg_new(&envoy_api_v2_DiscoveryRequest_msginit, arena);
}
UPB_INLINE envoy_api_v2_DiscoveryRequest *envoy_api_v2_DiscoveryRequest_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_DiscoveryRequest *ret = envoy_api_v2_DiscoveryRequest_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_DiscoveryRequest_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_DiscoveryRequest_serialize(const envoy_api_v2_DiscoveryRequest *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_DiscoveryRequest_msginit, arena, len);
}

UPB_INLINE upb_strview envoy_api_v2_DiscoveryRequest_version_info(const envoy_api_v2_DiscoveryRequest *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)); }
UPB_INLINE const struct envoy_api_v2_core_Node* envoy_api_v2_DiscoveryRequest_node(const envoy_api_v2_DiscoveryRequest *msg) { return UPB_FIELD_AT(msg, const struct envoy_api_v2_core_Node*, UPB_SIZE(24, 48)); }
UPB_INLINE upb_strview const* envoy_api_v2_DiscoveryRequest_resource_names(const envoy_api_v2_DiscoveryRequest *msg, size_t *len) { return (upb_strview const*)_upb_array_accessor(msg, UPB_SIZE(32, 64), len); }
UPB_INLINE upb_strview envoy_api_v2_DiscoveryRequest_type_url(const envoy_api_v2_DiscoveryRequest *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)); }
UPB_INLINE upb_strview envoy_api_v2_DiscoveryRequest_response_nonce(const envoy_api_v2_DiscoveryRequest *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(16, 32)); }
UPB_INLINE const struct google_rpc_Status* envoy_api_v2_DiscoveryRequest_error_detail(const envoy_api_v2_DiscoveryRequest *msg) { return UPB_FIELD_AT(msg, const struct google_rpc_Status*, UPB_SIZE(28, 56)); }

UPB_INLINE void envoy_api_v2_DiscoveryRequest_set_version_info(envoy_api_v2_DiscoveryRequest *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryRequest_set_node(envoy_api_v2_DiscoveryRequest *msg, struct envoy_api_v2_core_Node* value) {
  UPB_FIELD_AT(msg, struct envoy_api_v2_core_Node*, UPB_SIZE(24, 48)) = value;
}
UPB_INLINE struct envoy_api_v2_core_Node* envoy_api_v2_DiscoveryRequest_mutable_node(envoy_api_v2_DiscoveryRequest *msg, upb_arena *arena) {
  struct envoy_api_v2_core_Node* sub = (struct envoy_api_v2_core_Node*)envoy_api_v2_DiscoveryRequest_node(msg);
  if (sub == NULL) {
    sub = (struct envoy_api_v2_core_Node*)upb_msg_new(&envoy_api_v2_core_Node_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_DiscoveryRequest_set_node(msg, sub);
  }
  return sub;
}
UPB_INLINE upb_strview* envoy_api_v2_DiscoveryRequest_mutable_resource_names(envoy_api_v2_DiscoveryRequest *msg, size_t *len) {
  return (upb_strview*)_upb_array_mutable_accessor(msg, UPB_SIZE(32, 64), len);
}
UPB_INLINE upb_strview* envoy_api_v2_DiscoveryRequest_resize_resource_names(envoy_api_v2_DiscoveryRequest *msg, size_t len, upb_arena *arena) {
  return (upb_strview*)_upb_array_resize_accessor(msg, UPB_SIZE(32, 64), len, UPB_SIZE(8, 16), UPB_TYPE_STRING, arena);
}
UPB_INLINE bool envoy_api_v2_DiscoveryRequest_add_resource_names(envoy_api_v2_DiscoveryRequest *msg, upb_strview val, upb_arena *arena) {
  return _upb_array_append_accessor(
      msg, UPB_SIZE(32, 64), UPB_SIZE(8, 16), UPB_TYPE_STRING, &val, arena);
}
UPB_INLINE void envoy_api_v2_DiscoveryRequest_set_type_url(envoy_api_v2_DiscoveryRequest *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryRequest_set_response_nonce(envoy_api_v2_DiscoveryRequest *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(16, 32)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryRequest_set_error_detail(envoy_api_v2_DiscoveryRequest *msg, struct google_rpc_Status* value) {
  UPB_FIELD_AT(msg, struct google_rpc_Status*, UPB_SIZE(28, 56)) = value;
}
UPB_INLINE struct google_rpc_Status* envoy_api_v2_DiscoveryRequest_mutable_error_detail(envoy_api_v2_DiscoveryRequest *msg, upb_arena *arena) {
  struct google_rpc_Status* sub = (struct google_rpc_Status*)envoy_api_v2_DiscoveryRequest_error_detail(msg);
  if (sub == NULL) {
    sub = (struct google_rpc_Status*)upb_msg_new(&google_rpc_Status_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_DiscoveryRequest_set_error_detail(msg, sub);
  }
  return sub;
}

/* envoy.api.v2.DiscoveryResponse */

UPB_INLINE envoy_api_v2_DiscoveryResponse *envoy_api_v2_DiscoveryResponse_new(upb_arena *arena) {
  return (envoy_api_v2_DiscoveryResponse *)upb_msg_new(&envoy_api_v2_DiscoveryResponse_msginit, arena);
}
UPB_INLINE envoy_api_v2_DiscoveryResponse *envoy_api_v2_DiscoveryResponse_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_DiscoveryResponse *ret = envoy_api_v2_DiscoveryResponse_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_DiscoveryResponse_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_DiscoveryResponse_serialize(const envoy_api_v2_DiscoveryResponse *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_DiscoveryResponse_msginit, arena, len);
}

UPB_INLINE upb_strview envoy_api_v2_DiscoveryResponse_version_info(const envoy_api_v2_DiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(4, 8)); }
UPB_INLINE const struct google_protobuf_Any* const* envoy_api_v2_DiscoveryResponse_resources(const envoy_api_v2_DiscoveryResponse *msg, size_t *len) { return (const struct google_protobuf_Any* const*)_upb_array_accessor(msg, UPB_SIZE(32, 64), len); }
UPB_INLINE bool envoy_api_v2_DiscoveryResponse_canary(const envoy_api_v2_DiscoveryResponse *msg) { return UPB_FIELD_AT(msg, bool, UPB_SIZE(0, 0)); }
UPB_INLINE upb_strview envoy_api_v2_DiscoveryResponse_type_url(const envoy_api_v2_DiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(12, 24)); }
UPB_INLINE upb_strview envoy_api_v2_DiscoveryResponse_nonce(const envoy_api_v2_DiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(20, 40)); }
UPB_INLINE const struct envoy_api_v2_core_ControlPlane* envoy_api_v2_DiscoveryResponse_control_plane(const envoy_api_v2_DiscoveryResponse *msg) { return UPB_FIELD_AT(msg, const struct envoy_api_v2_core_ControlPlane*, UPB_SIZE(28, 56)); }

UPB_INLINE void envoy_api_v2_DiscoveryResponse_set_version_info(envoy_api_v2_DiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(4, 8)) = value;
}
UPB_INLINE struct google_protobuf_Any** envoy_api_v2_DiscoveryResponse_mutable_resources(envoy_api_v2_DiscoveryResponse *msg, size_t *len) {
  return (struct google_protobuf_Any**)_upb_array_mutable_accessor(msg, UPB_SIZE(32, 64), len);
}
UPB_INLINE struct google_protobuf_Any** envoy_api_v2_DiscoveryResponse_resize_resources(envoy_api_v2_DiscoveryResponse *msg, size_t len, upb_arena *arena) {
  return (struct google_protobuf_Any**)_upb_array_resize_accessor(msg, UPB_SIZE(32, 64), len, UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, arena);
}
UPB_INLINE struct google_protobuf_Any* envoy_api_v2_DiscoveryResponse_add_resources(envoy_api_v2_DiscoveryResponse *msg, upb_arena *arena) {
  struct google_protobuf_Any* sub = (struct google_protobuf_Any*)upb_msg_new(&google_protobuf_Any_msginit, arena);
  bool ok = _upb_array_append_accessor(
      msg, UPB_SIZE(32, 64), UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, &sub, arena);
  if (!ok) return NULL;
  return sub;
}
UPB_INLINE void envoy_api_v2_DiscoveryResponse_set_canary(envoy_api_v2_DiscoveryResponse *msg, bool value) {
  UPB_FIELD_AT(msg, bool, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryResponse_set_type_url(envoy_api_v2_DiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(12, 24)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryResponse_set_nonce(envoy_api_v2_DiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(20, 40)) = value;
}
UPB_INLINE void envoy_api_v2_DiscoveryResponse_set_control_plane(envoy_api_v2_DiscoveryResponse *msg, struct envoy_api_v2_core_ControlPlane* value) {
  UPB_FIELD_AT(msg, struct envoy_api_v2_core_ControlPlane*, UPB_SIZE(28, 56)) = value;
}
UPB_INLINE struct envoy_api_v2_core_ControlPlane* envoy_api_v2_DiscoveryResponse_mutable_control_plane(envoy_api_v2_DiscoveryResponse *msg, upb_arena *arena) {
  struct envoy_api_v2_core_ControlPlane* sub = (struct envoy_api_v2_core_ControlPlane*)envoy_api_v2_DiscoveryResponse_control_plane(msg);
  if (sub == NULL) {
    sub = (struct envoy_api_v2_core_ControlPlane*)upb_msg_new(&envoy_api_v2_core_ControlPlane_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_DiscoveryResponse_set_control_plane(msg, sub);
  }
  return sub;
}

/* envoy.api.v2.DeltaDiscoveryRequest */

UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest *envoy_api_v2_DeltaDiscoveryRequest_new(upb_arena *arena) {
  return (envoy_api_v2_DeltaDiscoveryRequest *)upb_msg_new(&envoy_api_v2_DeltaDiscoveryRequest_msginit, arena);
}
UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest *envoy_api_v2_DeltaDiscoveryRequest_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_DeltaDiscoveryRequest *ret = envoy_api_v2_DeltaDiscoveryRequest_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_DeltaDiscoveryRequest_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_DeltaDiscoveryRequest_serialize(const envoy_api_v2_DeltaDiscoveryRequest *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_DeltaDiscoveryRequest_msginit, arena, len);
}

UPB_INLINE const struct envoy_api_v2_core_Node* envoy_api_v2_DeltaDiscoveryRequest_node(const envoy_api_v2_DeltaDiscoveryRequest *msg) { return UPB_FIELD_AT(msg, const struct envoy_api_v2_core_Node*, UPB_SIZE(16, 32)); }
UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryRequest_type_url(const envoy_api_v2_DeltaDiscoveryRequest *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)); }
UPB_INLINE upb_strview const* envoy_api_v2_DeltaDiscoveryRequest_resource_names_subscribe(const envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) { return (upb_strview const*)_upb_array_accessor(msg, UPB_SIZE(24, 48), len); }
UPB_INLINE upb_strview const* envoy_api_v2_DeltaDiscoveryRequest_resource_names_unsubscribe(const envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) { return (upb_strview const*)_upb_array_accessor(msg, UPB_SIZE(28, 56), len); }
UPB_INLINE const envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry* const* envoy_api_v2_DeltaDiscoveryRequest_initial_resource_versions(const envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) { return (const envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry* const*)_upb_array_accessor(msg, UPB_SIZE(32, 64), len); }
UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryRequest_response_nonce(const envoy_api_v2_DeltaDiscoveryRequest *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)); }
UPB_INLINE const struct google_rpc_Status* envoy_api_v2_DeltaDiscoveryRequest_error_detail(const envoy_api_v2_DeltaDiscoveryRequest *msg) { return UPB_FIELD_AT(msg, const struct google_rpc_Status*, UPB_SIZE(20, 40)); }

UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_set_node(envoy_api_v2_DeltaDiscoveryRequest *msg, struct envoy_api_v2_core_Node* value) {
  UPB_FIELD_AT(msg, struct envoy_api_v2_core_Node*, UPB_SIZE(16, 32)) = value;
}
UPB_INLINE struct envoy_api_v2_core_Node* envoy_api_v2_DeltaDiscoveryRequest_mutable_node(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_arena *arena) {
  struct envoy_api_v2_core_Node* sub = (struct envoy_api_v2_core_Node*)envoy_api_v2_DeltaDiscoveryRequest_node(msg);
  if (sub == NULL) {
    sub = (struct envoy_api_v2_core_Node*)upb_msg_new(&envoy_api_v2_core_Node_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_DeltaDiscoveryRequest_set_node(msg, sub);
  }
  return sub;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_set_type_url(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryRequest_mutable_resource_names_subscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) {
  return (upb_strview*)_upb_array_mutable_accessor(msg, UPB_SIZE(24, 48), len);
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryRequest_resize_resource_names_subscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t len, upb_arena *arena) {
  return (upb_strview*)_upb_array_resize_accessor(msg, UPB_SIZE(24, 48), len, UPB_SIZE(8, 16), UPB_TYPE_STRING, arena);
}
UPB_INLINE bool envoy_api_v2_DeltaDiscoveryRequest_add_resource_names_subscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_strview val, upb_arena *arena) {
  return _upb_array_append_accessor(
      msg, UPB_SIZE(24, 48), UPB_SIZE(8, 16), UPB_TYPE_STRING, &val, arena);
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryRequest_mutable_resource_names_unsubscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) {
  return (upb_strview*)_upb_array_mutable_accessor(msg, UPB_SIZE(28, 56), len);
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryRequest_resize_resource_names_unsubscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t len, upb_arena *arena) {
  return (upb_strview*)_upb_array_resize_accessor(msg, UPB_SIZE(28, 56), len, UPB_SIZE(8, 16), UPB_TYPE_STRING, arena);
}
UPB_INLINE bool envoy_api_v2_DeltaDiscoveryRequest_add_resource_names_unsubscribe(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_strview val, upb_arena *arena) {
  return _upb_array_append_accessor(
      msg, UPB_SIZE(28, 56), UPB_SIZE(8, 16), UPB_TYPE_STRING, &val, arena);
}
UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry** envoy_api_v2_DeltaDiscoveryRequest_mutable_initial_resource_versions(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t *len) {
  return (envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry**)_upb_array_mutable_accessor(msg, UPB_SIZE(32, 64), len);
}
UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry** envoy_api_v2_DeltaDiscoveryRequest_resize_initial_resource_versions(envoy_api_v2_DeltaDiscoveryRequest *msg, size_t len, upb_arena *arena) {
  return (envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry**)_upb_array_resize_accessor(msg, UPB_SIZE(32, 64), len, UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, arena);
}
UPB_INLINE struct envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry* envoy_api_v2_DeltaDiscoveryRequest_add_initial_resource_versions(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_arena *arena) {
  struct envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry* sub = (struct envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry*)upb_msg_new(&envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_msginit, arena);
  bool ok = _upb_array_append_accessor(
      msg, UPB_SIZE(32, 64), UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, &sub, arena);
  if (!ok) return NULL;
  return sub;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_set_response_nonce(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)) = value;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_set_error_detail(envoy_api_v2_DeltaDiscoveryRequest *msg, struct google_rpc_Status* value) {
  UPB_FIELD_AT(msg, struct google_rpc_Status*, UPB_SIZE(20, 40)) = value;
}
UPB_INLINE struct google_rpc_Status* envoy_api_v2_DeltaDiscoveryRequest_mutable_error_detail(envoy_api_v2_DeltaDiscoveryRequest *msg, upb_arena *arena) {
  struct google_rpc_Status* sub = (struct google_rpc_Status*)envoy_api_v2_DeltaDiscoveryRequest_error_detail(msg);
  if (sub == NULL) {
    sub = (struct google_rpc_Status*)upb_msg_new(&google_rpc_Status_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_DeltaDiscoveryRequest_set_error_detail(msg, sub);
  }
  return sub;
}

/* envoy.api.v2.DeltaDiscoveryRequest.InitialResourceVersionsEntry */

UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_new(upb_arena *arena) {
  return (envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *)upb_msg_new(&envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_msginit, arena);
}
UPB_INLINE envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *ret = envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_serialize(const envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_msginit, arena, len);
}

UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_key(const envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)); }
UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_value(const envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)); }

UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_set_key(envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry_set_value(envoy_api_v2_DeltaDiscoveryRequest_InitialResourceVersionsEntry *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)) = value;
}

/* envoy.api.v2.DeltaDiscoveryResponse */

UPB_INLINE envoy_api_v2_DeltaDiscoveryResponse *envoy_api_v2_DeltaDiscoveryResponse_new(upb_arena *arena) {
  return (envoy_api_v2_DeltaDiscoveryResponse *)upb_msg_new(&envoy_api_v2_DeltaDiscoveryResponse_msginit, arena);
}
UPB_INLINE envoy_api_v2_DeltaDiscoveryResponse *envoy_api_v2_DeltaDiscoveryResponse_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_DeltaDiscoveryResponse *ret = envoy_api_v2_DeltaDiscoveryResponse_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_DeltaDiscoveryResponse_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_DeltaDiscoveryResponse_serialize(const envoy_api_v2_DeltaDiscoveryResponse *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_DeltaDiscoveryResponse_msginit, arena, len);
}

UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryResponse_system_version_info(const envoy_api_v2_DeltaDiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)); }
UPB_INLINE const envoy_api_v2_Resource* const* envoy_api_v2_DeltaDiscoveryResponse_resources(const envoy_api_v2_DeltaDiscoveryResponse *msg, size_t *len) { return (const envoy_api_v2_Resource* const*)_upb_array_accessor(msg, UPB_SIZE(24, 48), len); }
UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryResponse_type_url(const envoy_api_v2_DeltaDiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)); }
UPB_INLINE upb_strview envoy_api_v2_DeltaDiscoveryResponse_nonce(const envoy_api_v2_DeltaDiscoveryResponse *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(16, 32)); }
UPB_INLINE upb_strview const* envoy_api_v2_DeltaDiscoveryResponse_removed_resources(const envoy_api_v2_DeltaDiscoveryResponse *msg, size_t *len) { return (upb_strview const*)_upb_array_accessor(msg, UPB_SIZE(28, 56), len); }

UPB_INLINE void envoy_api_v2_DeltaDiscoveryResponse_set_system_version_info(envoy_api_v2_DeltaDiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE envoy_api_v2_Resource** envoy_api_v2_DeltaDiscoveryResponse_mutable_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, size_t *len) {
  return (envoy_api_v2_Resource**)_upb_array_mutable_accessor(msg, UPB_SIZE(24, 48), len);
}
UPB_INLINE envoy_api_v2_Resource** envoy_api_v2_DeltaDiscoveryResponse_resize_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, size_t len, upb_arena *arena) {
  return (envoy_api_v2_Resource**)_upb_array_resize_accessor(msg, UPB_SIZE(24, 48), len, UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, arena);
}
UPB_INLINE struct envoy_api_v2_Resource* envoy_api_v2_DeltaDiscoveryResponse_add_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, upb_arena *arena) {
  struct envoy_api_v2_Resource* sub = (struct envoy_api_v2_Resource*)upb_msg_new(&envoy_api_v2_Resource_msginit, arena);
  bool ok = _upb_array_append_accessor(
      msg, UPB_SIZE(24, 48), UPB_SIZE(4, 8), UPB_TYPE_MESSAGE, &sub, arena);
  if (!ok) return NULL;
  return sub;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryResponse_set_type_url(envoy_api_v2_DeltaDiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)) = value;
}
UPB_INLINE void envoy_api_v2_DeltaDiscoveryResponse_set_nonce(envoy_api_v2_DeltaDiscoveryResponse *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(16, 32)) = value;
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryResponse_mutable_removed_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, size_t *len) {
  return (upb_strview*)_upb_array_mutable_accessor(msg, UPB_SIZE(28, 56), len);
}
UPB_INLINE upb_strview* envoy_api_v2_DeltaDiscoveryResponse_resize_removed_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, size_t len, upb_arena *arena) {
  return (upb_strview*)_upb_array_resize_accessor(msg, UPB_SIZE(28, 56), len, UPB_SIZE(8, 16), UPB_TYPE_STRING, arena);
}
UPB_INLINE bool envoy_api_v2_DeltaDiscoveryResponse_add_removed_resources(envoy_api_v2_DeltaDiscoveryResponse *msg, upb_strview val, upb_arena *arena) {
  return _upb_array_append_accessor(
      msg, UPB_SIZE(28, 56), UPB_SIZE(8, 16), UPB_TYPE_STRING, &val, arena);
}

/* envoy.api.v2.Resource */

UPB_INLINE envoy_api_v2_Resource *envoy_api_v2_Resource_new(upb_arena *arena) {
  return (envoy_api_v2_Resource *)upb_msg_new(&envoy_api_v2_Resource_msginit, arena);
}
UPB_INLINE envoy_api_v2_Resource *envoy_api_v2_Resource_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  envoy_api_v2_Resource *ret = envoy_api_v2_Resource_new(arena);
  return (ret && upb_decode(buf, size, ret, &envoy_api_v2_Resource_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *envoy_api_v2_Resource_serialize(const envoy_api_v2_Resource *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &envoy_api_v2_Resource_msginit, arena, len);
}

UPB_INLINE upb_strview envoy_api_v2_Resource_version(const envoy_api_v2_Resource *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)); }
UPB_INLINE const struct google_protobuf_Any* envoy_api_v2_Resource_resource(const envoy_api_v2_Resource *msg) { return UPB_FIELD_AT(msg, const struct google_protobuf_Any*, UPB_SIZE(16, 32)); }
UPB_INLINE upb_strview envoy_api_v2_Resource_name(const envoy_api_v2_Resource *msg) { return UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)); }
UPB_INLINE upb_strview const* envoy_api_v2_Resource_aliases(const envoy_api_v2_Resource *msg, size_t *len) { return (upb_strview const*)_upb_array_accessor(msg, UPB_SIZE(20, 40), len); }

UPB_INLINE void envoy_api_v2_Resource_set_version(envoy_api_v2_Resource *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE void envoy_api_v2_Resource_set_resource(envoy_api_v2_Resource *msg, struct google_protobuf_Any* value) {
  UPB_FIELD_AT(msg, struct google_protobuf_Any*, UPB_SIZE(16, 32)) = value;
}
UPB_INLINE struct google_protobuf_Any* envoy_api_v2_Resource_mutable_resource(envoy_api_v2_Resource *msg, upb_arena *arena) {
  struct google_protobuf_Any* sub = (struct google_protobuf_Any*)envoy_api_v2_Resource_resource(msg);
  if (sub == NULL) {
    sub = (struct google_protobuf_Any*)upb_msg_new(&google_protobuf_Any_msginit, arena);
    if (!sub) return NULL;
    envoy_api_v2_Resource_set_resource(msg, sub);
  }
  return sub;
}
UPB_INLINE void envoy_api_v2_Resource_set_name(envoy_api_v2_Resource *msg, upb_strview value) {
  UPB_FIELD_AT(msg, upb_strview, UPB_SIZE(8, 16)) = value;
}
UPB_INLINE upb_strview* envoy_api_v2_Resource_mutable_aliases(envoy_api_v2_Resource *msg, size_t *len) {
  return (upb_strview*)_upb_array_mutable_accessor(msg, UPB_SIZE(20, 40), len);
}
UPB_INLINE upb_strview* envoy_api_v2_Resource_resize_aliases(envoy_api_v2_Resource *msg, size_t len, upb_arena *arena) {
  return (upb_strview*)_upb_array_resize_accessor(msg, UPB_SIZE(20, 40), len, UPB_SIZE(8, 16), UPB_TYPE_STRING, arena);
}
UPB_INLINE bool envoy_api_v2_Resource_add_aliases(envoy_api_v2_Resource *msg, upb_strview val, upb_arena *arena) {
  return _upb_array_append_accessor(
      msg, UPB_SIZE(20, 40), UPB_SIZE(8, 16), UPB_TYPE_STRING, &val, arena);
}

#ifdef __cplusplus
}  /* extern "C" */
#endif

#include "upb/port_undef.inc"

#endif  /* ENVOY_API_V2_DISCOVERY_PROTO_UPB_H_ */
