# LUC
LUC is a congestion control algorithm based on swap-regret-minimizing techniques. In our experiments, we implement LUC through Linux kernel 5.4.0 based on the congestion control plane ([CCP](https://ccp-project.github.io/)). With CCP, developers can write congestion control algorithms with Rust or Python in a safe user-space environment instead of writing C and risking crashing your kernel. CCP has two main entities, one is the CCP-kernel module, and the other is the user-space CCP algorithm. LUC is implemented as the user-space CCP algorithm, which inputs the statistics from CCP-kernel and outputs the congestion window/rates back to the kernel.

## Experiment: Emulation on Mininet
The experiments are based on two tools, i.e., [CCP](https://ccp-project.github.io/) and [Mininet](http://mininet.org/). CCP is used to implement LUC, and Mininet is the emulation tool to run experiments.
Furthermore, we recommend running the experiments on Linux kernel 5.4.0, as the recommended Linux kernel version of [CCP Kernel Datapath](https://github.com/ccp-project/ccp-kernel) is 5.4.0. 

In the paper, we run Mninet experiments to compare LUC with CUBIC and [BBR2](https://github.com/google/bbr/blob/v2alpha/README.md). CUBIC is the default congestion control algorithm in Linux Kernel 5.4.0. BBR2 is not included in the Linux kernel and needs to be compiled and installed.

In the following, we give step-by-step instructions on how to run the experiments.

### Step 1:  Install BBR2
There are two ways to install BBR2:
1. Manually build and install by following the instructions on https://github.com/google/bbr/blob/v2alpha/README.md.

First, we need to install the tools for compilation:

```
apt install -y build-essential libncurses5-dev git
apt -y build-dep linux
```

Then, download BBR2 and compile it by
```
git clone -o google-bbr -b v2alpha  https://github.com/google/bbr.git
cd bbr
make menuconfig
```
Then, go to Networking support ---> Networking options ---> TCP: advanced congestion control ---> BBR2 TCP (M). Save and exit. Next, we start compiling by

```
make deb-pkg
```


2. Download the compiled kernels that have already installed BBRv2 (we provide binary packages with BBR2 compiled for Debian/Ubuntu under this repo's "build" folder). 



If you choose the second way, you can run the following commands to replace the kernel (we have tested that the following kernel works for ubuntu 18.04 LTS):

```
sudo dpkg -i linux-headers-5.4.0-rc6_5.4.0-rc6-2_amd64.deb
sudo dpkg -i linux-image-5.4.0-rc6_5.4.0-rc6-2_amd64.deb
```

Next, enable the Grub menu for switching kernels. Edit the file /etc/default/grub, and find the following two lines:
```
GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=0
```
Change the two lines to
```
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=30
```
Save the changes and update grub by
```
sudo update-grub
```

Then restart the system.  In the Grub menu, select the Advanced options for Ubuntu and then select the corresponding kernel to boot the system.

Next, add the following two lines to /etc/sysctl.conf:
```
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr2
```
Make the two lines effective by `sudo sysctl -p`.

### Step 2: Install CCP
The instructions for installing CCP can be found on their website (https://ccp-project.github.io/ccp-guide/setup/index.html). However, when implementing LUC, we found that some APIs are updated, but the instructions on the official website are not updated to date. Therefore, we provide an instruction to install CCP as follows:

1. Install Rust
`curl https://sh.rustup.rs -sSf | sh -s -- -y -v --default-toolchain nightly`
2. Compile and run the Linux kernel module for CCP
```
git clone https://github.com/ccp-project/ccp-kernel.git
cd ccp-kernel
git submodule update --init --recursive
make
sudo ./ccp_kernel_load ipc=0
```
where ipc=0 is to use netlink sockets. To check whether CCP has been enabled, we can check by the following command:

```
sysctl net.ipv4.tcp_available_congestion_control
```
If you see "net.ipv4.tcp_available_congestion_control = reno cubic bbr2 ccp", the environment setup for both BBR2 and CCP-kernel is successful. 

The CCP-kernel module will report statistics to the user-space CCP algorithms. The user-space CCP algorithm determines a congestion window/rate and passes it back to the CCP-kernel.

3. To run python-based CCP algorithms and plot results, we need to install pyportus, cython, numpy, matplotlib, and pandas
```
sudo apt install python3-pip
sudo pip3 install pyportus numpy cython matplotlib pandas
```

If it shows an error message "python setup.py egg_info failed", run the following commands first:
```
sudo pip3 install setuptools-rust
sudo pip3 install --upgrade pip
```

4. Then, we can run the LUC algorithm by first compiling MAB and running LUC with sudo

```
python3 setup.py build_ext --inplace
```
```
sudo python3 luc.py

```
Now, CCP-kernel will report statistics to LUC. LUC will decide on the congestion window/rate and pass it back to CCP-kernel.


### Step 3: Install Mininet
We need to install it from the source. First, get the source code by
```
git clone https://github.com/mininet/mininet
```
Then, install it by using the script:
```
cd mininet
sudo python3 PYTHON=python3 util/install.sh -a
```




### Step 4: Run the experiments
1. The dumbell topology
Run the script dumbell.py by
```
sudo python3 dumbell.py
```
The results will be saved in the ''logs'' folder. To plot the logs, run the script plot_dumbell.py by
```
python3 plot_dumbell.py
```


2. The parkinglot topology
Run the script parkinglot.py by
```
sudo python3 parkinglot.py
```
The results will be saved in the ''logs'' folder. To plot the logs, run the script plot_dumbell.py by
```
python3 plot_parkinglot.py
```

The figures will be saved as eps in the ''results'' folder.

Before running each experiment, we can use `sudo mn -c` to clear the Mininet environment.

## Experiments with Pantheon
To run Pantheon, Python 2 is requried, and please ensure the default python environment is python 2.

We also use [Patheon](https://pantheon.stanford.edu/) to verify the performance of LUC with real-world traces. The real-world traces used in our paper can be found at https://github.com/ravinet/mahimahi/tree/master/traces. 

The setup and usage of Patheon can be found at https://github.com/StanfordSNR/pantheon. 

As the offcial source code is end of support, we give a convenient instruction here on playing luc on Pantheon with a comparison to CUBIC, BBR2 and Vivace. We have configured those four algorithms in our forked repo for Pantheon with real-world traces at https://github.com/Zhiming-Huang/pantheon.


To install dependencies, go to folder pantheon/tools, and run install_deps.sh.

Once installed, we can set up schemes by
```
src/experiments/setup.py --setup --all
```

Go to folder src/experiments/, and  run locally with real-world traces:
```
src/experiments/test.py local --all --uplink-trace Verizon-LTE-driving.up --downlink-trace Verizon-LTE-driving.down --run--times 5 
```

To visualize the results, go to folder src/analysis, and run
```
python ./analyze.py
```

The results will be saved in the folder src/experiments/data.
