# PRE :
# Execute deploy_lwip_dpdk script

# PARAMETERS :
# First parameter is the content length of the HTTP response
# Second parameter is the listening port number

cp main.c ~/tinyhttpd-lwip-dpdk/
cp lwipopts.h ~/tinyhttpd-lwip-dpdk/
cd
cd tinyhttpd-lwip-dpdk/
make 

content_len=$1
port_number=$2
interfacenum="$(cat myinterfacenum)"
addr="$(cat myaddr)"
gw="$(cat mygw)"
mask="$(cat mymask)"

echo $content_len
echo $port_number
echo $interfacenum
echo $addr
echo $gw
echo $mask

LD_LIBRARY_PATH=./dpdk/install/lib/x86_64-linux-gnu ./app -l 0-1 --proc-type=primary --file-prefix=pmd1 --allow=$interfacenumber -- -a $addr -g $gw -m $mask -l $content_len -p $port_number
