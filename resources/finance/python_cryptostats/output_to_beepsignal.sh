export password=bbbtFn98MJfFX4v7cOtg
export user=telef@cryptostats.net
export host=ftp.beepsignal.com
lftp -e 'debug;mput /home/stats/output/*.jpg;bye' -u "$user,$password" "ftp://$host/"  
