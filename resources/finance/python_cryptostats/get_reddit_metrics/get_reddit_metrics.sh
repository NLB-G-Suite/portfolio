set -x
DIR='/home/stats/get_reddit_metrics/output'
for k in `cat /home/stats/get_reddit_metrics/subreddits.list`
do
wget "redditmetrics.com/r/$k" -O $DIR/outfile_$k
echo date,Subscriber Growth > $DIR/outfile_subscriber-growth_$k
cat $DIR/outfile_$k | sed "s/element: 'subscriber-growth',/STARTING/g" | sed "s/element: 'total-subscribers',/ENDING/" | sed -ne '/^                    STARTING/,/^                            ENDING/p' | grep "{y:" | sed 's/            {y: //' | sed "s/'//g" | sed 's/ a: //' | sed 's/},//' | sed 's/}//' >> $DIR/outfile_subscriber-growth_$k
echo date,Total Subscribers > $DIR/outfile_total-subscribers_$k
cat $DIR/outfile_$k | sed "s/element: 'total-subscribers',/STARTING/g" | sed "s/labels: \['Subscribers'\]/ENDING/g" |  sed -ne '/^                            STARTING/,/^                                    ENDING/p' | grep "{y:" | sed 's/            {y: //' | sed "s/'//g" | sed 's/ a: //' | sed 's/},//' | sed 's/}//' >> $DIR/outfile_total-subscribers_$k
sleep 45
done
/usr/bin/python3 -u /home/stats/get_reddit_metrics/reddit_subscribers_to_jpg.py
