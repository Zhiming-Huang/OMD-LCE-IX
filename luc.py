import sys
import numpy as np
import MAB
import pyportus as portus



class LUCFlow:
    def __init__(self, datapath, datapath_info):
        self.datapath = datapath
        self.datapath_info = datapath_info
        self.rttbefore = 0
        self.cwndset = [34000 * i for i in range(7,12)]  #as CCP does not support rate change well, we pre-defined 5 cwnd as 5 different rates
        self.maxcwnd = self.cwndset[-1]
        self.MAB = MAB.MAB(len(self.cwndset),2)
        self.action = self.MAB.draw_action()
        self.cwnd = self.cwndset[self.action]
       
        self.datapath.set_program("default", [("Cwnd", int(self.cwnd))])
        
    def on_report(self, r):
        if self.rttbefore == 0:
            self.rttbefore = r.rtt
        #print(f"the ack: {r.acked} the loss:{r.loss}")
            reward = max((self.cwnd -  r.loss)/ self.maxcwnd,0)
        else:
            rttdiff = r.rtt - self.rttbefore
            reward = max((self.cwnd - self.cwnd/self.rttbefore * rttdiff - 100*self.datapath_info.mss* r.loss)/ self.maxcwnd,0)
            self.rttbefore = r.rtt
        #print(f"the action: {self.action} the rtt diff: {self.diffrtt} the reward:{reward} rate:{self.sndrate}")
        self.MAB.update_dist(self.action, reward)
        self.action = self.MAB.draw_action()
        self.cwnd = self.cwndset[self.action]
        #print(f"the reward {reward} the cwnd: {self.cwnd} the dis {self.MAB.p}")
        #print(self.cwnd)
        self.datapath.update_field("Cwnd", int(self.cwnd))
            
            


class LUC(portus.AlgBase):
    def datapath_programs(self):
        return {
            "default": """\
                (def (Report
                    (volatile acked 0)
                    (volatile sacked 0)
                    (volatile loss 0)
                    (volatile timeout false)
                    (volatile rtt 0)
                    (volatile inflight 0)
                    (volatile rate 0)
                ))
                (when true
                    (:= Report.inflight Flow.packets_in_flight)
                    (:= Report.rtt Flow.rtt_sample_us)
                    (:= Report.acked (+ Report.acked Ack.bytes_acked))
                    (:= Report.sacked (+ Report.sacked Ack.packets_misordered))
                    (:= Report.loss Ack.lost_pkts_sample)
                    (:= Report.timeout Flow.was_timeout)
                    (:= Report.rate Flow.rate_outgoing)
                    (fallthrough)
                )
                (when (> Micros Flow.rtt_sample_us)
                    (report)
                    (:= Micros 0)
                )
            """
        }

    def new_flow(self, datapath, datapath_info):
        return LUCFlow(datapath, datapath_info)


alg = LUC()

portus.start("netlink", alg)
