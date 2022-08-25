# Benchmarking-Enzyme-Classifiers

## Section 1: Steps of using the parallelization workflow 

### ECpred

1. Download ECpred from the website - https://github.com/cansyl/ECPred 
2. Install ECpred according to the instructions. Please note, the folder is nearly 10GB in size. 
3. The directory after successful installation should look like this -
![file_1](https://user-images.githubusercontent.com/66162359/182935588-fff9c14e-0729-4382-80f1-ad19c302d05b.PNG)

4. Copy the ECPred.sh and sample_file to the directory 
![file_2](https://user-images.githubusercontent.com/66162359/182936062-ebd85ffa-1dfc-4d1f-a5be-ecc202572e0e.PNG)

5. Run the command - 
```
./ECPred.sh sample_file
```

The output to the console should look like this - 
![file_3](https://user-images.githubusercontent.com/66162359/182936178-a4715972-e783-46bc-bcdb-af223786e9ef.PNG)

After the run is over the result file named - 'sample_result.txt' should look like this - 
![file_4](https://user-images.githubusercontent.com/66162359/182936553-eeef5ca4-54b5-4ed5-b2cf-0372b39f3c25.PNG)


6. To test a larger number of sequence, format the sequence according to sample_file and run the above command replacing sample_file with your file containing sequences. 

### DeepEC

1. Go to the website - https://bitbucket.org/kaistsystemsbiology/deepec/src/master/
2. Clone the repository by command - 
```
git clone https://bitbucket.org/kaistsystemsbiology/deepec.git
```
3. Create and activate conda enviornment following the instruction in the README.md file - 
```
conda env create -f environment.yml
conda activate deepec
```
4. Run the provided bash script deepec.sh with the sample file provided. 
```
./deepec.sh sample_file
```
5. The result will be written in a text file named deepec_result.txt
6. To test a larger number of sequence, format the sequence according to sample_file and run the above command replacing sample_file with your file containing sequences. 

### Deepre 

1. Go to the website - http://www.cbrc.kaust.edu.sa/DEEPre/
2. In the designated field input sequences in standard FASTA format 

### BENZ-ws 

1. Go to website - https://benzdb.biocomp.unibo.it/
2. Input sequences in standard FASTA format. 
