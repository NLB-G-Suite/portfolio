set -x
echo started probability ranges $1 $2 > /home/logs/probabilityranges_$1_$2.log
timefame=$1
asset=$2
/usr/bin/flock -xn /flock/probability_ranges_$1_$2.lck  /usr/bin/python3 -u /home/stats/probabilityranges/probabilityranges.py $1 $2 
