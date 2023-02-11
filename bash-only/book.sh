scp -r projects/Grid5000-Helper/bash-only/ nancy.g5k
scp -r bash-only/ root@gros-114:/home/
ssh nancy.g5k
oarsub -I -t deploy -l nodes=1,walltime=4 -p " cluster = 'gros' "
kadeploy3 ubuntu2204-min
oarstat -u 
cat /var/lib/oar/<id>
ssh root@gros-xx