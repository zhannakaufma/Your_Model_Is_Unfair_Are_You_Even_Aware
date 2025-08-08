# Your_Model_Is_Unfair_Are_You_Even_Aware
This is everything required to replicate all results from the paper *Your Model Is Unfair, Are You Even Aware? Inverse Relationship Between Comprehension and Trust in Explainability Visualizations of Biased ML Models*

## Abstract
Systems relying on ML have become ubiquitous, but so has biased behavior within them. Research shows that bias significantly affects stakeholders' trust in systems and how they use them. Further, stakeholders of different backgrounds view and trust the same systems differently. Thus, how ML models' behavior is explained plays a key role in comprehension and trust. We survey explainability visualizations, creating a taxonomy of design characteristics. We conduct user studies to evaluate five state-of-the-art visualization tools (LIME, SHAP, CP, Anchors, and ELI5) for model explainability, measuring how taxonomy characteristics affect comprehension, bias perception, and trust for non-expert ML users. Surprisingly, we find an inverse relationship between comprehension and trust: the better users understand the models, the less they trust them. We investigate the cause and find that this relationship is strongly mediated by bias perception: more comprehensible visualizations increase people's perception of bias, and increased bias perception reduces trust. We confirm this relationship is causal: Manipulating explainability visualizations to control comprehension, bias perception, and trust, we show that visualization design can significantly (p<0.001) increase comprehension, increase perceived bias, and reduce trust. Conversely, reducing perceived model bias, either by improving model fairness or by adjusting visualization design, significantly increases trust even when comprehension remains high.  Our work advances understanding of how comprehension affects trust and systematically investigates visualization\'s role in facilitating responsible ML applications. 


## Files
Key files and directories:
- `Colab code for visualization generation/`: This is the code for generating all of the visualizations we used in our surveys (paper figures 4 and 8). The code is separated out by explainability type for all surveys used in RQ2 (SHAP Force, SHAP Waterfall, ELI5, Ceteris-Paribus, LIME, Anchors). For RQ3, files are titled *Survey code for Followup Experiments*. Each file exists as a Jyupiter notebook to be run in Colab, a python file, and a PDF printout of a Colab run. 
- `Surveys/`: PDFs of all of the surveys described in our paper, generated using the above files.
- `Raw Results and Longtable Code/`: All of our data in raw form and in longtable form, and the scripts we used to generate our longtables from our raw data. To generate the main longtable file, `total_longtable.csv`, please run `all_longtable.sh` in this directory. This longtable file is used by `RQ2_RQ3_Stats_Script.Rmd` and `R_figures.Rmd`.
- `RQ2_RQ3_Stats_Script.Rmd`: R Script containing all statistical tests run on longtable data for research questions 2 and 3. 
- `RQ2_RQ3_Stats_Script.pdf`: Outputs of running the above R script printed to pdf via knit.
- `R_figures.Rmd`: R Script containing everything needed to generate paper figures 1 and 5.
- `R_figures.pdf`: Outputs of running the above R script printed to pdf via knit.
- `Qualitative Responses/`: Coded qualitative response data, and tableau files for generating paper figures 6 and 7. 
- `total_longtable.csv`: Longtable generated via `Raw Results and Longtable Code/` that includes all results and is used for the `Rmd` files.
- `Taxonomy.pdf`: Full taxonomy described in research question 1 applied to 26 different explainability tools. 
- `Disparate Impact Quantification.pdf`: Comparison of fair and unfair model outputs across gender and age demographic groups.
- `paper_figures`: Adobe Illustrator files used to make figures 1, 5, and 8 in the paper. 

## Dependencies and Requirements 
- All required software aside from Adobe Illustrator is free.
- For any `ipynb` Jyupiter notebook files, please use Google colab with a python 3 runtime type and a CPU hardware accelerator.
  - Colab should install any required dependencies, but we have also included a `requirements.txt` file 
- To run bash files that generate longtable code, please use a linux or OSX terminal with `python3` installed.
- For `Rmd` files, please run Rstudio (version >= 2024.09.1+394). All required libraries will be installed and loaded by these scripts.
- For `.twbx` tableau files, please open in Tableau Public (Version >= 2025.2.0 (20252.25.0514.2217))
- For `.ai` adobe illustrator files, please use Adobe illustrator.

## Replicating Statistical Results
Please run `RQ2_RQ3_Stats_Script.Rmd` in Rstudio. This script will install all required dependences.

## Generating Paper figures 
### Figure 1 
Use file `R_figures.Rmd`, and `paper_figures/figure-1.ai`
### Figure 2
Use file `Taxonomy.pdf`
### Figure 4 
Use files in `Colab code for visualization generation/`
#### 4a 
- Open `Survey code for SHAP Waterfall.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
#### 4b
- Open `Survey code for SHAP Force.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
#### 4c
- Open `Survey code for ELI5.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
#### 4d
- Open `Survey code for LIME.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
#### 4e
- Open `Survey code for Ceteris-Paribus.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
#### 4f
- Open `Survey code for Anchors.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"
- You will see figure 4a under "Generate a tutorial explanation"
### Figure 5 
Use file `R_figures.Rmd` and `paper_figures/figure-5.ai`
### Figures 6 - 7
Use files in `Qualitative Responses/`
#### Figure 6
- Open `Figure_6.twbx` in Tableau Public.
#### Figure 7
- Open `Figure_7.twbx` in Tableau Public.
### Figure 8 
Use files in `Colab code for visualization generation/` and `paper_figures/figure-8.ai`
- Open `Survey code for Followup Experiments.ipynb` in Google colab
- Upload `Umbrella.csv` to "Files" to make it available to the script 
- Under runtime, select "Run all"

## Paper Citation
> Z. Kaufman, M. Endres, C. Xiong Bearfield, and Y. Brun. 2025. *Your Model Is Unfair, Are You Even Aware? Inverse Relationship Between Comprehension and Trust in Explainability Visualizations of Biased ML Models*. TVCG. 

