#/usr/bin/bash

mkdir files

mv $1 files/

cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/files

split -l 10 $1 l

for fil in *;do

mv $fil $fil.fasta
done

wait

for file in *.fasta;do
sleep 3
mv $file /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/
cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred
java -jar ECPred.jar weighted $file /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/ temp/ ${file}_results.tsv &
sleep 3
cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/files
done

wait

echo Prediction completed
sleep 2

cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/

cat *.tsv >> sample_result.txt



echo DONE



