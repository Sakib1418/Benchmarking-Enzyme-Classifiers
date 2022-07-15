# Benchmarking-Enzyme-Classifiers

## Section 1: Steps of using the parallelization workflow 

### ECpred

1. Download ECpred from the website - https://github.com/cansyl/ECPred 
2. Install ECpred according to the instructions. 
3. Copy the ECPred.sh and sample_file to the directory 
4. Run the command - 
```
./ECPred.sh sample_file
```

### DeepEC

1. Clone the repository by command - 
```
git clone https://bitbucket.org/kaistsystemsbiology/deepec.git
```
2. Create and activate conda enviornment following the instruction in the README.md file. 
3. Run the provided bash script deepec.sh with the sample file provided. 
```
./deepec.sh sample_file
```

5. To test a larger number of sequence, format the sequence according to sample_file and run the above command replacing sample_file with your file containing sequences. 

## Section 2: Steps of using the visualization workflow

1. Download the Uniprot data from <https://www.uniprot.org/uniprot/?query=*&fil=> and name it uniprot_data.csv
2. Format the result according to result.csv 
3. put uniprot_data.csv and result.csv in the same directory where visualization.py exists
4. Run visualization.py 
```
$python visualization.py
```
5. For sample run, download the data from https://drive.google.com/file/d/1c-HkhGPwfzuiVNTxlx16DMlJzmGrGq6P/view?usp=sharing and extract the file in the same directory where the visulalization.py script exists. Then run the visualization.py like step 4. 
