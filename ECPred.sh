#/usr/bin/bash
rm -r files
echo files deleted
mkdir files

cp $1 files/

cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/files

split -l 2 $1 l
echo list of files are 
ls

rm $1
echo list of files after deleting main file

for fil in *;do
echo $fil
mv $fil $fil.fasta
done

wait

for file in *.fasta;
do
sleep .1
mv $file /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/
cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred
java -jar ECPred.jar weighted $file /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/ temp/ ${file}_results.tsv &
sleep .25
cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/files
done

wait

echo Prediction completed


cd /home/reuel/Desktop/Sakib/ML/classification/ECpred/ECPred/

ls *.tsv
rm sample_result.txt

for res in *.tsv;
do
cat $res | tail -1 >> sample_result.txt
done

wait 

rm *.fasta
rm *.tsv
echo DONE
