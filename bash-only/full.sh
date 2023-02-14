dhclient eno2

apt update
apt -y install net-tools git gcc openssl libssl-dev linux-headers-$(uname -r) bc libnuma1 libnuma-dev libpcre3 libpcre3-dev zlib1g-dev meson  python3-pip unzip python-is-python3 netcat

# check interfaces
ifconfig >> res_ifconfig

mkdir /data
cd /data/ 

# build fstack
wget https://github.com/F-Stack/f-stack/archive/refs/tags/v1.22.zip
unzip v1.22.zip
mv f-stack-1.22 f-stack
pip3 install pyelftools
cd /data/f-stack/dpdk/
meson -Denable_kmods=true build
ninja -C build
ninja -C build install
cd /data/

# pkg config version
wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz
tar xzvf pkg-config-0.29.2.tar.gz
cd pkg-config-0.29.2/
./configure --with-internal-glib
make
make install
ln -s /usr/local/bin/pkg-config /usr/bin/pkg-config



# mount hugepages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mkdir /mnt/huge
mount -t hugetlbfs nodev /mnt/huge

# userspace networking : one step towards enabling it
modprobe uio
insmod /data/f-stack/dpdk/build/kernel/linux/igb_uio/igb_uio.ko
insmod /data/f-stack/dpdk/build/kernel/linux/kni/rte_kni.ko carrier=on

cd /data/f-stack/dpdk/usertools/ 
ifconfig


# https://github.com/F-Stack/f-stack/issues/586
cd /data/
export FF_PATH=/data/f-stack
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/local/lib64/pkgconfig:/usr/lib/pkgconfig:/data/f-stack/dpdk/build/meson-private

#cd /data/f-stack/lib/
#make  # It will produce an error but it's normal
#cd /data/f-stack/mk
#sed '/WERROR?= -Werror -Wno-unused-variable/s/^/#/' kern.pre.mk > kern.pre.mk.new
#mv kern.pre.mk.new kern.pre.mk

# link dpdk lib
pkg-config --cflags libdpdk
pkg-config --libs libdpdk

# install api
cd /data/f-stack/lib/
make
make install 

# install nginx app
cd /data/f-stack/app/nginx-1.16.1
sed -i '548,$d' ./src/event/modules/ngx_ff_module.c
echo 'int
gettimeofday(struct timeval *tv, void *__restrict tzp)
{
    struct timezone *tz = (struct timezone *) tzp;
    if (unlikely(inited == 0)) {
        return SYSCALL(gettimeofday)(tv, tz);
    }

    return ff_gettimeofday(tv, tz);
}' >> ./src/event/modules/ngx_ff_module.c
./configure --prefix=/usr/local/nginx_fstack --with-ff_module
make
make install

# install tools such as ifconfig
cd /data/f-stack/tools/
make
make install

#cd /data/f-stack
#cp config.ini f-stack.conf
#mv f-stack.conf /etc/f-stack.conf

#cd example/
#make
#./helloworld --conf /etc/f-stack.conf --proc-type=primary &

# check available NICs
cd /data/f-stack/dpdk/usertools
python3 dpdk-devbind.py --status    

echo "python dpdk-devbind.py --bind=igb_uio <name_of_interface_to_bind>"
# python dpdk-devbind.py --bind=igb_uio <name_of_interface_to_bind>




export myaddr=`ifconfig eno1 | grep "inet" | grep -v ":" | awk -F ' '  '{print $2}'`
export mymask=`ifconfig eno1 | grep "netmask" | awk -F ' ' '{print $4}'`
export mybc=`ifconfig eno1 | grep "broadcast" | awk -F ' ' '{print $6}'`
export myhw=`ifconfig eno1 | grep "ether" | awk -F ' ' '{print $2}'`
export mygw=`route -n | grep 0.0.0.0 | grep eno1 | grep UG | awk -F ' ' '{print $2}'`


sed "s/addr=192.168.1.2/addr=${myaddr}/" -i /data/f-stack/config.ini
sed "s/netmask=255.255.255.0/netmask=${mymask}/" -i /data/f-stack/config.ini
sed "s/broadcast=192.168.1.255/broadcast=${mybc}/" -i /data/f-stack/config.ini
sed "s/gateway=192.168.1.1/gateway=${mygw}/" -i /data/f-stack/config.ini


sed "s/#\[kni\]/\[kni\]/" -i /data/f-stack/config.ini
sed "s/#enable=1/enable=1/" -i /data/f-stack/config.ini
sed "s/#method=reject/method=reject/" -i /data/f-stack/config.ini
sed "s/#tcp_port=80/tcp_port=80/" -i /data/f-stack/config.ini
sed "s/#vlanstrip=1/vlanstrip=1/" -i /data/f-stack/config.ini

cp /data/f-stack/config.ini /usr/local/nginx_fstack/conf/f-stack.conf

ifconfig eno1 down
python /data/f-stack/dpdk/usertools/dpdk-devbind.py --bind=igb_uio eno1

/usr/local/nginx_fstack/sbin/nginx

sleep 10
ifconfig veth0 ${myaddr}  netmask ${mymask}  broadcast ${mybc} hw ether ${myhw}
route add -net 0.0.0.0 gw ${mygw} dev veth0
echo 1 > /sys/class/net/veth0/carrier # if `carrier=on` not set while `insmod rte_kni.ko`.
