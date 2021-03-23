# GINI
./jobs/topd_tuning/primer.sh 'surgical' 'gini' 100 20 25 'accuracy' 1.0 3 1440 'short'
./jobs/topd_tuning/primer.sh 'vaccine' 'gini' 50 20 5 'accuracy' 1.0 6 1440 'short'
./jobs/topd_tuning/primer.sh 'adult' 'gini' 50 20 5 'accuracy' 1.0 3 1440 'short'
./jobs/topd_tuning/primer.sh 'bank_marketing' 'gini' 100 20 25 'roc_auc' 1.0 3 1440 'short'
./jobs/topd_tuning/primer.sh 'flight_delays' 'gini' 250 20 25 'roc_auc' 1.0 18 1440 'short'
./jobs/topd_tuning/primer.sh 'diabetes' 'gini' 250 20 5 'accuracy' 1.0 18 1440 'short'
./jobs/topd_tuning/primer.sh 'no_show' 'gini' 250 20 10 'roc_auc' 1.0 18 1440 'short'
./jobs/topd_tuning/primer.sh 'olympics' 'gini' 250 20 5 'roc_auc' 1.0 35 1440 'short'
./jobs/topd_tuning/primer.sh 'census' 'gini' 100 20 25 'roc_auc' 1.0 18 1440 'short'
./jobs/topd_tuning/primer.sh 'credit_card' 'gini' 250 20 5 'average_precision' 1.0 9 1440 'short'
./jobs/topd_tuning/primer.sh 'twitter' 'gini' 100 20 5 'roc_auc' 0.5 35 1440 'short'
./jobs/topd_tuning/primer.sh 'synthetic' 'gini' 50 20 10 'accuracy' 0.25 30 1440 'short'
./jobs/topd_tuning/primer.sh 'ctr' 'gini' 100 10 50 'roc_auc' 0.25 10 1440 'short'
./jobs/topd_tuning/primer.sh 'higgs' 'gini' 50 20 10 'accuracy' 0.025 70 1440 'short'


# ENTROPY
# ./jobs/topd_tuning/primer.sh 'surgical' 'entropy' 100 20 50 'accuracy' 1.0 3 1440 'short'
# ./jobs/topd_tuning/primer.sh 'vaccine' 'entropy' 250 20 5 'accuracy' 1.0 6 1440 'short'
# ./jobs/topd_tuning/primer.sh 'adult' 'entropy' 50 20 5 'accuracy' 1.0 3 1440 'short'
# ./jobs/topd_tuning/primer.sh 'bank_marketing' 'entropy' 100 10 10 'roc_auc' 1.0 3 1440 'short'
# ./jobs/topd_tuning/primer.sh 'flight_delays' 'entropy' 250 20 50 'roc_auc' 1.0 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'diabetes' 'entropy' 100 20 5 'accuracy' 1.0 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'no_show' 'entropy' 250 20 10 'roc_auc' 1.0 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'olympics' 'entropy' 250 20 5 'roc_auc' 1.0 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'census' 'entropy' 100 20 25 'roc_auc' 1.0 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'credit_card' 'entropy' 250 10 25 'average_precision' 1.0 9 1440 'short'
# ./jobs/topd_tuning/primer.sh 'ctr' 'entropy' 100 10 25 'roc_auc' 0.25 10 1440 'short'
# ./jobs/topd_tuning/primer.sh 'twitter' 'entropy' 100 20 5 'roc_auc' 0.5 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'synthetic' 'entropy' 50 20 10 'accuracy' 0.25 15 1440 'short'
# ./jobs/topd_tuning/primer.sh 'higgs' 'entropy' 50 20 10 'accuracy' 0.025 70 1440 'short'
