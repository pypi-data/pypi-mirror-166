/*******************************************************************************
* Copyright 2020 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

/* <copyright>

  Contact Information:
  https://software.intel.com/content/www/us/en/develop/tools/vtune-profiler.html

  BSD LICENSE

  Copyright (c) 2005-2014 Intel Corporation. All rights reserved.
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.
    * Neither the name of Intel Corporation nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</copyright> */

#ifndef _ITTNOTIFY_TYPES_H_
#define _ITTNOTIFY_TYPES_H_

typedef enum ___itt_group_id
{
    __itt_group_none      = 0,
    __itt_group_legacy    = 1<<0,
    __itt_group_control   = 1<<1,
    __itt_group_thread    = 1<<2,
    __itt_group_mark      = 1<<3,
    __itt_group_sync      = 1<<4,
    __itt_group_fsync     = 1<<5,
    __itt_group_jit       = 1<<6,
    __itt_group_model     = 1<<7,
    __itt_group_splitter_min = 1<<7,
    __itt_group_counter   = 1<<8,
    __itt_group_frame     = 1<<9,
    __itt_group_stitch    = 1<<10,
    __itt_group_heap      = 1<<11,
    __itt_group_splitter_max = 1<<12,
    __itt_group_structure = 1<<12,
    __itt_group_suppress = 1<<13,
    __itt_group_arrays    = 1<<14,
    __itt_group_all       = -1
} __itt_group_id;

#pragma pack(push, 8)

typedef struct ___itt_group_list
{
    __itt_group_id id;
    const char*    name;
} __itt_group_list;

#pragma pack(pop)

#define ITT_GROUP_LIST(varname) \
    static __itt_group_list varname[] = {       \
        { __itt_group_all,       "all"       }, \
        { __itt_group_control,   "control"   }, \
        { __itt_group_thread,    "thread"    }, \
        { __itt_group_mark,      "mark"      }, \
        { __itt_group_sync,      "sync"      }, \
        { __itt_group_fsync,     "fsync"     }, \
        { __itt_group_jit,       "jit"       }, \
        { __itt_group_model,     "model"     }, \
        { __itt_group_counter,   "counter"   }, \
        { __itt_group_frame,     "frame"     }, \
        { __itt_group_stitch,    "stitch"    }, \
        { __itt_group_heap,      "heap"      }, \
        { __itt_group_structure, "structure" }, \
        { __itt_group_suppress,  "suppress"  }, \
        { __itt_group_arrays,    "arrays"    }, \
        { __itt_group_none,      NULL        }  \
    }

#endif /* _ITTNOTIFY_TYPES_H_ */
