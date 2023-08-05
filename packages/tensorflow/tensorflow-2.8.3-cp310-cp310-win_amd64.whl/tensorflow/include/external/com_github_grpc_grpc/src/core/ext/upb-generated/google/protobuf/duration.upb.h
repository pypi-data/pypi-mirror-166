/* This file was generated by upbc (the upb compiler) from the input
 * file:
 *
 *     google/protobuf/duration.proto
 *
 * Do not edit -- your changes will be discarded when the file is
 * regenerated. */

#ifndef GOOGLE_PROTOBUF_DURATION_PROTO_UPB_H_
#define GOOGLE_PROTOBUF_DURATION_PROTO_UPB_H_

#include "upb/generated_util.h"
#include "upb/msg.h"
#include "upb/decode.h"
#include "upb/encode.h"

#include "upb/port_def.inc"

#ifdef __cplusplus
extern "C" {
#endif

struct google_protobuf_Duration;
typedef struct google_protobuf_Duration google_protobuf_Duration;
extern const upb_msglayout google_protobuf_Duration_msginit;


/* google.protobuf.Duration */

UPB_INLINE google_protobuf_Duration *google_protobuf_Duration_new(upb_arena *arena) {
  return (google_protobuf_Duration *)upb_msg_new(&google_protobuf_Duration_msginit, arena);
}
UPB_INLINE google_protobuf_Duration *google_protobuf_Duration_parse(const char *buf, size_t size,
                        upb_arena *arena) {
  google_protobuf_Duration *ret = google_protobuf_Duration_new(arena);
  return (ret && upb_decode(buf, size, ret, &google_protobuf_Duration_msginit, arena)) ? ret : NULL;
}
UPB_INLINE char *google_protobuf_Duration_serialize(const google_protobuf_Duration *msg, upb_arena *arena, size_t *len) {
  return upb_encode(msg, &google_protobuf_Duration_msginit, arena, len);
}

UPB_INLINE int64_t google_protobuf_Duration_seconds(const google_protobuf_Duration *msg) { return UPB_FIELD_AT(msg, int64_t, UPB_SIZE(0, 0)); }
UPB_INLINE int32_t google_protobuf_Duration_nanos(const google_protobuf_Duration *msg) { return UPB_FIELD_AT(msg, int32_t, UPB_SIZE(8, 8)); }

UPB_INLINE void google_protobuf_Duration_set_seconds(google_protobuf_Duration *msg, int64_t value) {
  UPB_FIELD_AT(msg, int64_t, UPB_SIZE(0, 0)) = value;
}
UPB_INLINE void google_protobuf_Duration_set_nanos(google_protobuf_Duration *msg, int32_t value) {
  UPB_FIELD_AT(msg, int32_t, UPB_SIZE(8, 8)) = value;
}

#ifdef __cplusplus
}  /* extern "C" */
#endif

#include "upb/port_undef.inc"

#endif  /* GOOGLE_PROTOBUF_DURATION_PROTO_UPB_H_ */
