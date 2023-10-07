#!/usr/bin/python     
                                                                       
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=4 ):
        linkopts = dict(bw=50, delay='10ms', loss = 0, max_queue_size=100)
        linkopts2 = dict(bw=50, delay='10ms', loss = 0)
        switch1 = self.addSwitch( 's1' )
        switch2 = self.addSwitch('s2')
        self.addLink(switch1, switch2, **linkopts)    
        
        # Each host gets 50%/n of system CPU
        h1 = self.addHost( 'h1',cpu=.5/n, ip='10.0.0.1')
        h2 = self.addHost( 'h2',cpu=.5/n, ip='10.0.0.2')
        self.addLink(h1, switch1, **linkopts2)
        self.addLink(h2, switch1, **linkopts2)
        h3 = self.addHost( 'h3',cpu=.5/n, ip='10.0.0.3')
        h4 = self.addHost( 'h4',cpu=.5/n, ip='10.0.0.4')
        self.addLink(h3, switch2, **linkopts2)
        self.addLink(h4, switch2, **linkopts2)



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
    h1, h2, h3, h4 = net.get( 'h1', 'h2', 'h3', 'h4' )
    
    h3.sendCmd('iperf -s -p 5000')

    h4.sendCmd('iperf -s -p 5001')

    sleep(3)
    if num == 0:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z ccp -i 1 -t 30 -e > ./logs/ccp1.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z ccp -i 1 -t 30 -e > ./logs/ccp2.log &')

    if num == 1:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z bbr2 -i 1 -t 30 -e > ./logs/bbr1.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z bbr2 -i 1 -t 30 -e > ./logs/bbr2.log &')
 
    if num == 2:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z cubic -i 1 -t 30 -e > ./logs/cubic1.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/cubic2.log &')
 
    if num == 3:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z ccp -i 1 -t 30 -e > ./logs/ccp1bbr2.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z bbr2 -i 1 -t 30 -e > ./logs/bbr2ccp1.log &')
        
    if num == 4:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z ccp -i 1 -t 30 -e > ./logs/ccp1cubic2.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/cubic2ccp1.log &')
        
    if num == 5:
        h1.sendCmd('iperf -c 10.0.0.3 -p 5000 -Z bbr2 -i 1 -t 30 -e > ./logs/bbr1cubic2.log &')

        h2.sendCmd('iperf -c 10.0.0.4 -p 5001 -Z cubic -i 1 -t 30 -e > ./logs/cubic2bbr1.log &')
        
    sleep(35)
    #CLI(net)
    
    #net.iperf( (h1, h3) )
    #h1.sendCmd('preprocessor.sh test_results1.json .')
    #h2.sendCmd('preprocessor.sh test_results2.json .')
    
    h1.terminate()
    h2.terminate()    
    h3.terminate()
    h4.terminate()
    
    
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
