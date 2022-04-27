#/usr/bin/bash

mkdir files

mv $1 files/

cd {path to ECpred folder}/files

split -l 10 $1 l

for fil in *;do

mv $fil $fil.fasta
done

wait

for file in *.fasta;do
sleep 3
mv $file {path to ECpred folder}
cd {path to ECpred folder}
java -jar ECPred.jar weighted $file {path to ECpred folder} temp/ ${file}_results.tsv &
sleep 3
cd {path to ECpred folder}/files
done

wait

echo Prediction completed
sleep 2

cd {path to ECpred folder}

cat *.tsv >> sample_result.txt



echo DONE



