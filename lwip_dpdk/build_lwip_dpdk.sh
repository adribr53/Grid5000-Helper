# PRE :
# ssh nantes.g5k
# Put the script in /home/<user>/public/Grid5000-Helper/lwip_dpdk folder
# oarsub -I -l nodes=2,walltime=4 -p "cluster = 'ecotype'"
# sudo-g5k -i
# cd /home/<user>/public/Grid5000-Helper/lwip_dpdk
# ./build_lwip_dpdk.sh

cd

# Attribute IP to interface eno2
dhclient eno2 

apt update
apt install -y build-essential net-tools meson python3-pip

# Build DPDK
pip3 install pyelftools
cd /root
wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz # once
tar xzvf pkg-config-0.29.2.tar.gz                                         # once
cd /root/pkg-config-0.29.2/          
./configure --with-internal-glib
make
make install

# hugepages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mkdir /mnt/huge
mount -t hugetlbfs nodev /mnt/huge

# Build lwip
cd /root/
git clone https://github.com/yasukata/tinyhttpd-lwip-dpdk.git # once
cd tinyhttpd-lwip-dpdk/
make # Produce error but it's normal
cp lwipopts.h ./lwip/lwip-2.1.3/src/include/lwip/
make

# Save IPs
ifconfig eno2 | grep "inet" | grep -v ":" | awk -F ' '  '{print $2}' > myaddr
route -n | grep 0.0.0.0 | grep UG | awk -F ' ' '{print $2}' > mygw
ifconfig eno2 | grep "netmask" | awk -F ' ' '{print $4}' > mymask

# Bind interface and save interface number
modprobe vfio-pci #(or modprobe uio + insmod ./x86_64-native-linux-gcc/kmod/igb_uio.ko) # Choose type of interface (vfio or uio)
./dpdk/dpdk-22.03/usertools/dpdk-devbind.py -s # Choose interface to bind
myinterfacenum=`./dpdk/dpdk-22.03/usertools/dpdk-devbind.py -s | grep "eno2" | grep -oP '^\S+' | cut -d" " -f1`
echo $myinterfacenum > myinterfacenum

ifconfig eno2 down
./dpdk/dpdk-22.03/usertools/dpdk-devbind.py -b vfio-pci $myinterfacenum #(eg: 0000:01:00.1)
