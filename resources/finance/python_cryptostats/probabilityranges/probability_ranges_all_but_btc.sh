DIR='/home/stats/probabilityranges'
for t in `cat $DIR/timeframes.list`
do
     for a in `/home/common/poloniex_alt_list.sh`
     do
          echo $DIR/probabilityranges.sh $t $a
          $DIR/probabilityranges.sh $t $a
     done
done
