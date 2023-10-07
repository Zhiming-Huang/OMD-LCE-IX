#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 19:45:17 2022

@author: zhiming
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns
import re


def read_iperf(filename):
    bandwith = []
    cwnd = []
    rtt = []
    with open(filename) as fp_in:
        for i, line in enumerate(fp_in):
            if "[ ID]" in line:
                continue
            if i >= 7:
                try:
                    
                    bandwith.append(float(re.findall(r"\d+", line.split('  ')[3])[0]))
                except:
                    bandwith.append(line.split(' ')[9])
                cwnd.append(int(line.split(' ')[-2].split('/')[0][0:-1]))
                rtt.append(int(line.split(' ')[-2].split('/')[1])/1000)
    bandwith.pop(-1)
    cwnd.pop(-1)
    rtt.pop(-1)
    bandwith.pop(0)
    cwnd.pop(0)
    rtt.pop(0)
    dic = {'throughput': bandwith, 'cwnd':cwnd, 'rtt':rtt}
    return pd.DataFrame(dic)


################################### Scenario 1 #########################
dfccp1 = read_iperf('./logs/parking_ccp1.log')
dfccp2 = read_iperf('./logs/parking_ccp2.log')
dfccp3 = read_iperf('./logs/parking_ccp3.log')

dfbbr1 = read_iperf('./logs/parking_bbr1.log')
dfbbr2 = read_iperf('./logs/parking_bbr2.log')
dfbbr3 = read_iperf('./logs/parking_bbr3.log')

dfcubic1 = read_iperf('./logs/parking_cubic1.log')
dfcubic2 = read_iperf('./logs/parking_cubic2.log')
dfcubic3 = read_iperf('./logs/parking_cubic3.log')

#sns.set('whitegrid')

###################Throughput  1################################
#############plot for h1
fig, ax = plt.subplots()
ax.plot(dfccp1['throughput'].ewm(com=10).mean(), '-', label = 'OMD-LCE-IX')
ax.plot(dfbbr1['throughput'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic1['throughput'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('Throughput (Mbps)',fontsize=20)
ax.set_ylim([0,45])
ax.grid(True)
ax.legend(fontsize=20, loc = 'best',fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_thru_h1.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
############plot for h2
fig, ax = plt.subplots()
ax.plot(dfccp2['throughput'].ewm(com=10).mean(), '-',  label = 'OMD-LCE-IX')
ax.plot(dfbbr2['throughput'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic2['throughput'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)', fontsize=20)
ax.set_ylabel('Throughput (Mbps)', fontsize=20)
ax.set_ylim([0,45])
ax.grid(True)
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_thru_h2.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)

############plot for h3
fig, ax = plt.subplots()
ax.plot(dfccp3['throughput'].ewm(com=10).mean(), '-',  label = 'OMD-LCE-IX')
ax.plot(dfbbr3['throughput'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic3['throughput'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('Throughput (Mbps)',fontsize=20)
ax.set_ylim([0,45])
ax.grid(True)
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_thru_h3.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)

################### RTT  1 ################################
#############plot for h1
fig, ax = plt.subplots()
ax.plot(dfccp1['rtt'].ewm(com=10).mean(), '-', label = 'OMD-LCE-IX')
ax.plot(dfbbr1['rtt'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic1['rtt'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
#ax.set_ylim([60,220])
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_rtt_h1.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
############plot for h2
fig, ax = plt.subplots()
ax.plot(dfccp2['rtt'].ewm(com=10).mean(), '-',  label = 'OMD-LCE-IX')
ax.plot(dfbbr2['rtt'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic2['rtt'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
#ax.set_ylim([60,220])
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_rtt_h2.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)

############plot for h4
fig, ax = plt.subplots()
ax.plot(dfccp3['rtt'].ewm(com=10).mean(), '-',  label = 'OMD-LCE-IX')
ax.plot(dfbbr3['rtt'].ewm(com=10).mean(), '-.', label = 'BBR2')
ax.plot(dfcubic3['rtt'].ewm(com=10).mean(), '--', label = 'CUBIC')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
#ax.set_ylim([60,220])
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_homoflow_rtt_h4.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)

################################### Scenario 2 #########################
dfbackccp1 = read_iperf('./logs/parking_backccp_ccp.log')
dfbackccp2 = read_iperf('./logs/parking_backccp_cubic.log')
dfbackccp3 = read_iperf('./logs/parking_backccp_bbr.log')

dfbackbbr1 = read_iperf('./logs/parking_backbbr_bbr.log')
dfbackbbr2 = read_iperf('./logs/parking_backbbr_cubic.log')
dfbackbbr3 = read_iperf('./logs/parking_backbbr_ccp.log')

dfbackcubic1 = read_iperf('./logs/parking_backcubic_cubic.log')
dfbackcubic2 = read_iperf('./logs/parking_backcubic_bbr.log')
dfbackcubic3 = read_iperf('./logs/parking_backcubic_ccp.log')


###################Throughput  2################################
#############plot for luc ######
fig, ax = plt.subplots()
ax.plot(dfbackccp1['throughput'].ewm(com=10).mean(), '-', label = 'h1 (OMD-LCE-IX)', color = 'tab:blue')
ax.plot(dfbackccp2['throughput'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)',  color ='tab:green')
ax.plot(dfbackccp3['throughput'].ewm(com=10).mean(), '-.', label = 'h4 (BBR2)', color ='tab:orange')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('Throughput (Mbps)',fontsize=20)
ax.grid(True)
ax.set_ylim([0,60])
ax.legend(fontsize=20, loc = 'best', fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_heteflow_thru_ccp.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for bbr######
fig, ax = plt.subplots()
ax.plot(dfbackbbr1['throughput'].ewm(com=10).mean(), '-.', label = 'h1 (BBR2)', color = 'tab:orange')
ax.plot(dfbackbbr2['throughput'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.plot(dfbackbbr3['throughput'].ewm(com=10).mean(), '-', label = 'h4 (OMD-LCE-IX)', color ='tab:blue')
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('Throughput (Mbps)',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.grid(True)
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
ax.set_ylim([0,60])
fig.savefig('./results/Park_heteflow_thru_bbr.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for cubic######
fig, ax = plt.subplots()
ax.plot(dfbackcubic1['throughput'].ewm(com=10).mean(), '--', label = 'h1 (CUBIC)',  color = 'tab:green')
ax.plot(dfbackcubic2['throughput'].ewm(com=10).mean(), '-.', label = 'h2 (BBR2)', color ='tab:orange')
ax.plot(dfbackcubic3['throughput'].ewm(com=10).mean(), '-', label = 'h4 (OMD-LCE-IX)', color ='tab:blue')
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('Throughput (Mbps)',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.grid(True)
ax.legend(fontsize=20,loc='best', fancybox=True, framealpha=0.5)
ax.set_ylim([0,60])
#ax.set_ylim([0,90])
fig.savefig('./results/Park_heteflow_thru_cubic.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)


###################RTT  2################################
#############plot for luc ######
fig, ax = plt.subplots()
ax.plot(dfbackccp1['rtt'].ewm(com=10).mean(), '-', label = 'h1 (OMD-LCE-IX)', color = 'tab:blue')
ax.plot(dfbackccp2['rtt'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)',  color ='tab:green')
ax.plot(dfbackccp3['rtt'].ewm(com=10).mean(), '-.', label = 'h4 (BBR2)', color ='tab:orange')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
ax.set_ylim([50,300])
fig.savefig('./results/Park_heteflow_rtt_ccp.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for bbr######
fig, ax = plt.subplots()
ax.plot(dfbackbbr1['rtt'].ewm(com=10).mean(), '-.', label = 'h1 (BBR2)', color = 'tab:orange')
ax.plot(dfbackbbr2['rtt'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.plot(dfbackbbr3['rtt'].ewm(com=10).mean(), '-', label = 'h4 (OMD-LCE-IX)', color ='tab:blue')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
ax.set_ylim([50,300])
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
fig.savefig('./results/Park_heteflow_rtt_bbr.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for cubic######
fig, ax = plt.subplots()
ax.plot(dfbackcubic1['rtt'].ewm(com=10).mean(), '--', label = 'h1 (CUBIC)',  color = 'tab:green')
ax.plot(dfbackcubic2['rtt'].ewm(com=10).mean(), '-.', label = 'h2 (BBR2)', color ='tab:orange')
ax.plot(dfbackcubic3['rtt'].ewm(com=10).mean(), '-', label = 'h4 (OMD-LCE-IX)', color ='tab:blue')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
ax.set_xlabel('Time (s)',fontsize=20)
ax.set_ylabel('RTT (ms)',fontsize=20)
ax.grid(True)
ax.legend(fontsize=20, fancybox=True, framealpha=0.5)
ax.set_ylim([50,300])
fig.savefig('./results/Park_heteflow_rtt_cubic.pdf', format='pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
