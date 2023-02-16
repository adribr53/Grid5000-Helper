# PRE :
# Execute deploy_lwip_dpdk script

# PARAMETERS :
# First parameter is the listening port number

cd 
cd tinyhttpd-lwip-dpdk/
port_number=$1
interfacenum="$(cat myinterfacenum)"
addr="$(cat myaddr)"
gw="$(cat mygw)"
mask="$(cat mymask)"

echo $port_number
echo $interfacenum
echo $addr
echo $gw
echo $mask

LD_LIBRARY_PATH=./dpdk/install/lib/x86_64-linux-gnu ./app -l 0-1 --proc-type=primary --file-prefix=pmd1 --allow=$interfacenumber -- -a $addr -g $gw -m $mask -l 1 -p $port_number
