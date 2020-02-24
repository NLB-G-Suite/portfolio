/usr/bin/flock -xn /flock/correlation_matrix_15m.lck sh -c '/usr/bin/python3 -u /home/stats/correlmatrix/correlation_matrix.py 15min'
/usr/bin/flock -xn /flock/correlation_matrix_30m.lck sh -c '/usr/bin/python3 -u /home/stats/correlmatrix/correlation_matrix.py 30min'
/usr/bin/flock -xn /flock/correlation_matrix_1h.lck sh -c '/usr/bin/python3 -u /home/stats/correlmatrix/correlation_matrix.py 1h'
/usr/bin/flock -xn /flock/correlation_matrix_4h.lck sh -c '/usr/bin/python3 -u /home/stats/correlmatrix/correlation_matrix.py 4h'
/usr/bin/flock -xn /flock/correlation_matrix_1d.lck sh -c '/usr/bin/python3 -u /home/stats/correlmatrix/correlation_matrix.py 1d'

