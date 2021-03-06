# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A simple memory monitor
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

import os
import psutil


class MemoryTracker(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Cbench, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        
        if msg.reason == ofp.OFPR_NO_MATCH:
            reason = 'NO MATCH'
        elif msg.reason == ofp.OFPR_ACTION:
            reason = 'ACTION'
        elif msg.reason == ofp.OFPR_INVALID_TTL:
            reason = 'INVALID TTL'
        else:
            reason = 'unknown'
        
        self.logger.debug('OFPPacketIn received: '
            'buffer_id=%x total_len=%d reason=%s '
            'table_id=%d cookie=%d match=%s data=%s',
            msg.buffer_id, msg.total_len, reason,
            msg.table_id, msg.cookie, msg.match,
            utils.hex_array(msg.data))

        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0]/2.**10    # K bytes  

        self.logger.info("MemTracker: %d K", memoryUse)
        
