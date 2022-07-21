#/usr/bin/bash

for a in $(seq 1 2 $(cat $1 | wc -l))

do
b=$(($a+1))
touch $(cat $1 | head -$a | tail -1).fasta
echo $(cat $1 | head -$a | tail -1) >> $(echo $(cat $1 | head -$a | tail -1)).fasta
echo $(cat $1 | head -$b | tail -1) >> $(echo $(cat $1 | head -$a | tail -1)).fasta
done
wait

for file in *.fasta;do
sleep .5
python deepec.py -i $file -o ${file}.tsv
sleep .5
done

wait

echo Prediction completed
sleep 2

for file in *.tsv;do
cd $file
cat *.txt | head -2 >> ../deepec_result.txt
cd ..
done

wait
for file in *.tsv;do
echo $file
rm -r $file
done

wait
for file in *.fasta;do
rm $file
done



echo DONE


