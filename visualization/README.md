# Steps for running the visualization workflow

1. Download the uniprot data and result from this link - https://drive.google.com/file/d/1kqYIoPYGLH-5oqKP9QI8y_ZOlnv3uHPg/view?usp=sharing
2. Extract the folders inside this directory. 
3. Run df_maker.py first to make all the relevant data tables. All the dataframes will be created at vis_result folder created. 
```
$python df_maker.py
```
4. Run the scripts to visualize the data. The images will be saved in vis_result folder. 

The file description are - 

| Script name  | Function |
| --------------- | ------------- |
| ECPred_result_15_12.csv  | Contains result of the enzyme prediction of whole uniprot database to date 15th December,2021 with ECPred classifier  |
| uniprot-reviewed_04_12.tab  | Contains actual EC number from Uniprot database  |
| df_maker.py | Creates all the necessary dataframes for analysis |
| overall_performance.py | Creates graph of performance summary of the classifier | 
| performance_wrt_changing_length.py | Creates graph of performance over increasing length | 
| performance_wrt_EC_number.py | Creates graph of performance in different EC number | 
| performance_wrt_aa_composition.py | Creates graph of performance with increasing amino acid compostion | 
| enzyme_non_enzyme_aa_ratio.py | Creates percent bar graph of enzyme and non enzyme over changing aa composition | 
| aa_distribution.py | Creates density plot of amino acid composition | 
