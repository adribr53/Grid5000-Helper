ssh nantes.g5k
oarsub -I -t deploy -l nodes=2,walltime=4 -p " cluster = 'ecotype' "
kadeploy3 -f $OAR_NODEFILE -k -e debian11-x64-nfs
uniq $OAR_NODEFILE | taktuk -d -1 -l root -f - broadcast exec [ 'dhclient eno2' ]

apt-get update
apt-get install build-essential

# Keep track of addresses of interface to bind
apt install net-tools
ip a (for ip address)
route -n (for gateway address and netmask)

# Build DPDK
apt install meson
apt install python3-pip
pip3 install pyelftools

wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz
tar xzvf pkg-config-0.29.2.tar.gz
cd pkg-config-0.29.2/
./configure --with-internal-glib
make
make install
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mkdir /mnt/huge
mount -t hugetlbfs nodev /mnt/huge

# Build lwip
cd /root/
git clone https://github.com/yasukata/tinyhttpd-lwip-dpdk.git
cd tinyhttpd-lwip-dpdk/
make # Produce error but it's normal
cp lwipopts.h /root/tinyhttpd-lwip-dpdk/lwip/lwip-2.1.3/src/include/lwip/
make

# Bind interface
modprobe vfio-pci (or modprobe uio + insmod ./x86_64-native-linux-gcc/kmod/igb_uio.ko) # Choose type of interface (vfio or uio)
./dpdk/dpdk-22.03/usertools/dpdk-devbind.py -s # Choose interface to bind
ifconfig <interface> down
./dpdk/dpdk-22.03/usertools/dpdk-devbind.py -b vfio-pci <interface_number> (eg: 0000:01:00.1)

# Run server
LD_LIBRARY_PATH=./dpdk/install/lib/x86_64-linux-gnu ./app -l 0-1 --proc-type=primary --file-prefix=pmd1 --allow=<interface_number> -- -a <ip_address> -g <gateway> -m <netmask> -l 1 -p <port_number>

# For instance :
LD_LIBRARY_PATH=./dpdk/install/lib/x86_64-linux-gnu ./app -l 0-1 --proc-type=primary --file-prefix=pmd1 --allow=0000:01:00.1 -- -a 172.16.194.41 -g 172.16.207.254 -m 255.255.240.0-l 1 -p 8080

# wrk benchmarking (to do on another machine)
apt-get update
apt-get install build-essential
git clone https://github.com/wg/wrk.git
make
./wrk http://<ip>:<port>/ -d 10 -t 1 -c 1 -L
