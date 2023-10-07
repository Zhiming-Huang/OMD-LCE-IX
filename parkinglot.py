#!/usr/bin/python     
                                                                       
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
#from mininet.cli import CLI
from time import sleep

class SingleSwitchTopo( Topo ):
    """        Node_1          Node_3         Node_5
                  \              |             /
                   \             |10ms        /10ms
                 5ms\            |           /
                     \      A    |    B     /
                   Router1 ---Router2--- Router3
                     /    10ms   |   10ms   \
                    /            |          \
               10ms/             |10ms      \ 5ms
                  /              |          \
             Node_2           Node_4       Node_6
"""
    def build( self, n=6 ):
        linkopts = dict(bw=50, delay='10ms', loss = 0, max_queue_size=100)
        linkopts2 = dict(bw=50, delay='10ms', loss = 0)
        linkopts3 = dict(bw=50, delay='5ms', loss = 0)
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')
        self.addLink(switch1, switch2, **linkopts)    
        self.addLink(switch2, switch3, **linkopts)    

        # Each host gets 50%/n of system CPU
        h1 = self.addHost( 'h1',cpu=.5/n, ip='10.0.0.1')
        h2 = self.addHost( 'h2',cpu=.5/n, ip='10.0.0.2')
        self.addLink(h1, switch1, **linkopts3)
        self.addLink(h2, switch1, **linkopts2)
        h3 = self.addHost( 'h3',cpu=.5/n, ip='10.0.0.3')
        h4 = self.addHost( 'h4',cpu=.5/n, ip='10.0.0.4')
        self.addLink(h3, switch2, **linkopts2)
        self.addLink(h4, switch2, **linkopts2)
        h5 = self.addHost( 'h5',cpu=.5/n, ip='10.0.0.5')
        h6 = self.addHost( 'h6',cpu=.5/n, ip='10.0.0.6')
        self.addLink(h5, switch3, **linkopts2)
        self.addLink(h6, switch3, **linkopts3)

def perfTest(num = 0):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo( n=4 )
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections( net.hosts )
    # print( "Testing network connectivity" )
    # net.pingAll()
    print( "Testing bandwidth" )
    h1, h2, h3, h4, h5, h6 = net.get( 'h1', 'h2', 'h3', 'h4', 'h5', 'h6')
    
    
# Flow 1: Node_1 <--> Node_6
# Flow 2: Node_2 <--> Node_3
# Flow 3: Node_4 <--> Node_5
    h6.sendCmd('iperf -s -p 5000')

    h3.sendCmd('iperf -s -p 5001')
    
    h5.sendCmd('iperf -s -p 5002')

    sleep(3)
    if num == 0:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z ccp -i 1 -t 30 -e > ./logs/parking_ccp1.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z ccp -i 1 -t 30 -e > ./logs/parking_ccp2.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z ccp -i 1 -t 30 -e > ./logs/parking_ccp3.log &')
        

    if num == 1:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z cubic -i 1 -t 30 -e > ./logs/parking_cubic1.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/parking_cubic2.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z cubic -i 1 -t 30 -e > ./logs/parking_cubic3.log &')

    if num == 2:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z bbr -i 1 -t 30 -e > ./logs/parking_bbr1.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z bbr -i 1 -t 30 -e > ./logs/parking_bbr2.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z bbr -i 1 -t 30 -e > ./logs/parking_bbr3.log &')
        
    if num == 3:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z ccp -i 1 -t 30 -e > ./logs/parking_backccp_ccp.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/parking_backccp_cubic.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z bbr -i 1 -t 30 -e > ./logs/parking_backccp_bbr.log &')
        
    if num == 4:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z bbr -i 1 -t 30 -e > ./logs/parking_backbbr_bbr.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/parking_backbbr_cubic.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z ccp -i 1 -t 30 -e > ./logs/parking_backbbr_ccp.log &')
        
    if num == 5:
        h1.sendCmd('iperf -c 10.0.0.6 -p 5000 -Z cubic -i 1 -t 30 -e > ./logs/parking_backcubic_cubic.log &')

        h2.sendCmd('iperf -c 10.0.0.3 -p 5001 -Z bbr -i 1 -t 30 -e > ./logs/parking_backcubic_bbr.log &')
        
        h4.sendCmd('iperf -c 10.0.0.5 -p 5002 -Z ccp -i 1 -t 30 -e > ./logs/parking_backcubic_ccp.log &')
        
    sleep(35)
    #CLI(net)
    
    #net.iperf( (h1, h3) )
    #h1.sendCmd('preprocessor.sh test_results1.json .')
    #h2.sendCmd('preprocessor.sh test_results2.json .')
    
    h1.terminate()
    h2.terminate()    
    h3.terminate()
    h4.terminate()
    h5.terminate()
    h6.terminate()    

    #sleep(10)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    perfTest(0)
    perfTest(1)
    perfTest(2)
    perfTest(3)
    perfTest(4)
    perfTest(5)
