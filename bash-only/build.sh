cd /data/
export FF_PATH=/data/f-stack
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/local/lib64/pkgconfig:/usr/lib/pkgconfig:/data/f-stack/dpdk/build/meson-private

#cd /data/f-stack/lib/
#make  # It will produce an error but it's normal
#cd /data/f-stack/mk
#sed '/WERROR?= -Werror -Wno-unused-variable/s/^/#/' kern.pre.mk > kern.pre.mk.new
#mv kern.pre.mk.new kern.pre.mk

cd /data/f-stack/lib/
pkg-config --cflags libdpdk
pkg-config --libs libdpdk
make
make install 

cd /data/f-stack/tools/
make
make install

cd /data/f-stack
cp config.ini f-stack.conf
mv f-stack.conf /etc/f-stack.conf

cd example/
make
./helloworld --conf /etc/f-stack.conf --proc-type=primary &