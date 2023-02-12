arg1=$1
arg2=$2
echo $2
cp setup_machine.sh ~/mount-g5k
scp -r ~/mount-g5k/* $1.g5k:/home/agiot/$2
ssh $1.g5k "sshfs -o idmap=user root@$2:/data /home/agiot"