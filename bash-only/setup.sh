apt update
apt -y install git gcc openssl libssl-dev linux-headers-$(uname -r) bc libnuma1 libnuma-dev libpcre3 libpcre3-dev zlib1g-dev meson  python3-pip unzip

mkdir /data
cd /data/ 
wget https://github.com/F-Stack/f-stack/archive/refs/tags/v1.22.zip
unzip v1.22.zip
mv f-stack-1.22 f-stack

pip3 install pyelftools
cd /data/f-stack/dpdk/
meson -Denable_kmods=true build
ninja -C build
ninja -C build install
cd /data/
wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz
tar xzvf pkg-config-0.29.2.tar.gz
cd pkg-config-0.29.2/
./configure --with-internal-glib
make
make install
ln -s /usr/local/bin/pkg-config /usr/bin/pkg-config
export FF_PATH=/data/f-stack
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/local/lib64/pkgconfig:/usr/lib/pkgconfig
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mkdir /mnt/huge
mount -t hugetlbfs nodev /mnt/huge
modprobe uio
insmod /data/f-stack/dpdk/build/kernel/linux/igb_uio/igb_uio.ko
insmod /data/f-stack/dpdk/build/kernel/linux/kni/rte_kni.ko carrier=on

cd /data/f-stack/dpdk/usertools/
apt install python-is-python3 
apt install net-tools
ifconfig
python3 dpdk-devbind.py --status    # Check available NICs

echo "python dpdk-devbind.py --bind=igb_uio <name_of_interface_to_bind>"
# python dpdk-devbind.py --bind=igb_uio <name_of_interface_to_bind>


