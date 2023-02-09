arg1=$1
arg2=$2
echo $2
ssh $1.g5k "mkdir -p $2"
cp setup_machine.sh ~/mount-$3
scp -r ~/mount-$3/* $1.g5k:/home/agiot/$2
ssh $1.g5k "mkdir -p $2"
ssh $1.g5k "ssh root@$2 "mkdir data""
ssh $1.g5k "sshfs -o idmap=user root@$2:/data /home/agiot/$2"