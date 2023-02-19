# PARAMETERS :
# First parameter is the content length of the HTTP response
# Second parameter is the listening port number

content_len=$1
port_number=$2
myaddr=`ifconfig eno2 | grep "inet" | grep -v ":" | awk -F ' '  '{print $2}'`
echo $content_len
echo $myaddr
echo $port_number

cp linux_stack_server.c ~/
cd
gcc linux_stack_server.c -o linux_stack_server -Wall -Werror
./linux_stack_server -l $content_len -a $myaddr -p $port_number
