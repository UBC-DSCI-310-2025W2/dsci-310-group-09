# dsci-310-group-09 — Online Shoppers Purchase Behavior Classification

# Introduction

This project develops machine learning classification models to predict whether an online shopping session results in a purchase. The analysis is based on the _Online Shoppers Purchasing Intention Dataset_, which contains features describing user behaviour such as page activity, session duration, and traffic source.

Predicting purchasing behavior is an important problem in e-commerce, as it enables businesses to better understand customer intent, improve conversion rates, and optimize website design. By leveraging user engagement metrics, this project aims to identify the most influential factors that drive purchase decisions.

The project emphasizes reproducibility and modular design, providing two fully reproducible workflows using **conda-lock** (for local environments) and **Docker** (for containerized execution).

# Findings
Our findings showed that engagement related features were the most important predictors of online shopping behaviour. PageValue in particular, has the greatest influence on the model's performance followed by ExitRates, ProductRelated_Duration, ProductRelated, and BounceRates. According to the SHAP summary plot, high PageValue is associated with a positive SHAP value whereas high ExitRate is related to a negative SHAP value. This is not surprising as users who viewed high value pages are more likely to make a purchase compared to those who frequently exit pages. Longer viewing time of product related pages also indicate higher likelihood of purchase, in addition, users who leave the website quickly (High BounceRates) is related to lower purchase. The month of November is also found to positively relate with higher purchase, which is likely due to holiday shopping behaviour and sales occurring in this particular month. 

This suggests e-commerce businesses should prioritize the user’s website engagement by capitalizing on high value pages and improving website design to maximize product related duration, which can reduce bounce rates and increase the likelihood of a purchase. For instance, offering exclusive deals or customized recommendations on high value pages. Additionally, configuring UX/UI interface to improve functionality and ease of use to keep users on the website.

# Dependencies
This project uses Python 3.10 with dependency management handled through a locked Conda environment (`conda-lock.yml`). All package versions are fully pinned to ensure reproducibility across different systems.

Alternatively, the analysis can be executed within the provided Docker container, which automatically installs all required dependencies at the correct versions. This ensures a consistent and reproducible computing environment regardless of the host machine.

Key dependencies include:

| Package        | Version | Purpose |
|----------------|--------|--------|
| python | 3.10 | Core programming language used for the project |
| numpy | 2.2.6 | Numerical computations and array operations |
| pandas | 2.3.3 | Data loading, cleaning, and manipulation |
| scikit-learn | 1.7.2 | Training classification models and evaluating performance |
| matplotlib | 3.10.8 | Creating visualizations for exploratory data analysis and results |
| shap | 0.49.1 | Interpreting model predictions using SHAP values |
| pytest | 9.0.2 | Unit testing framework for validating functions in `src/` |
| click | 8.3.1 | Command-line interface support for running scripts |
| pip | 26.0.1 | Package manager used to install Python dependencies |
| online-shoppers-tools | 0.1.0 | Package designed to support common tasks in data science workflows, such as cleaning and transforming data, converting boolean-like variables, analyzing class balances, generating feature importance plots, and evaluating classifications models with performance metrics |

All dependencies are pinned in the [conda-lock.yml](./conda-lock.yml) file.

# Project Structure
Below is the directory structure of the project, highlighting the distinction between `src/` and `source/`:

```bash
.
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── README.md
├── analysis
│   └── 310-group9_online-shoppers-classification.ipynb
├── conda-lock.yml
├── data
├── environment.yml
├── makefile
├── reports
│   ├── citations.bib
│   ├── online-shoppers-classification.html
│   └── online-shoppers-classification.qmd
│   
├── results
│   ├(include .png, .csv generated from makefile)
├── source
│   ├── 01_download_raw_data.py
│   ├── 02_data_cleaning.py
│   ├── 03_EDA_histogram.py
│   └── 04_model_output.py
├── src
│   ├── __init__.py
│   ├── calculate_class_balance.py
│   ├── convert_boolean_values.py
│   ├── create_feat_importance_plot.py
│   ├── data_validation.py
│   └── evaluate_model.py
└── tests
    ├── test_calculate_class_balance.py
    ├── test_convert_boolean_values.py
    ├── test_create_feat_importance_plot.py
    └── test_evaluate_model.py
```

## Key Distinction

- `src/`: Contains reusable, modular functions used throughout the project (e.g., preprocessing, model training, evaluation logic)
- `source/`: Contains scripts that call functions from `src/` to execute full pipeline steps (used by the Makefile).

# Reproducibility and Dependencies

- **Conda environment (locked):** `conda-lock.yml`  
- **Container definition:** `Dockerfile`  
- **Automated image publishing:** GitHub Actions builds and pushes the Docker image to Docker Hub when the `Dockerfile` or dependency files are updated on `main`.

---

## Option A: Run with conda-lock (recommended for local development)

Install conda-lock and create the environment. Run the code below one line at a time.

### 1. Set up Environment

```bash
conda install -c conda-forge conda-lock
conda-lock install -n online-shoppers conda-lock.yml
conda activate online-shoppers
```

## Option B: Run using Docker

The Docker image is defined in the root-level Dockerfile and is automatically built and pushed to Docker Hub through GitHub Actions whenever the Dockerfile or dependency files are updated on main.

### 1. Pull the Image

```bash
docker pull cjz115/dsci-310-group-09:latest
```

### 2. Run the Container 

```bash
docker run --rm -it \
  -v "$PWD":/home/work \
  -w /home/work \
  cjz115/dsci-310-group-09:latest \
  bash
```

### 3. Makefile Execution

Ensure you are inside the project environment using either option A or option B above:
- If using conda-lock: run `conda activate online-shoppers`
- If using docker: The makefile is available inside the container's working directory.

Once inside the project environment, run the following code to execute the entire analysis:

```bash
make all 
```

To execute specific steps in the pipeline, run the code below replacing "filename" with the actual filename on makefile:

```bash
make filename
```

To reset the analysis (remove all generated data files and results), run:

```bash
make clean
```

### 4. Quarto Report

The final analysis report is written in Quarto.

To open and render:

```bash
quarto render reports/online-shoppers-classification.qmd
```

### 5. Accessing the Report

The rendered report will be in `reports/online-shoppers-classification.html`

For Mac from repo root, run in terminal:

```bash
open reports/online-shoppers-classification.html
```

For Windows run:

```bash
start reports/online-shoppers-classification.html
```

It would open the .html for you.

# More on Condainer, tests, and data validation

## Stopping the Docker Container

When you are finished using the container, you can stop it in one of the following ways:

### 1. Stop directly in the terminal

If the container is running in your current terminal, simply type:

```bash
exit
```

This will stop the container immediately.

### 2. Stop using Docker commands

If the container is running in the background or another terminal

1. Find the container ID

```bash
docker ps
```

2. Stop the container

```bash
docker stop <container_id>
```

Replace `<container_id>` with the value shown under the **CONTAINER ID** column

## Running Tests

Unit tests for the core utility functions are maintained in the [online-shoppers-tools](https://github.com/UBC-DSCI-310-2025W2/online-shoppers-tools/tree/main) repository. These tests validate key components of the analysis pipeline. Please refer to that repository for instructions on how to run the tests.

Unit tests are also located in the [tests](./tests) directory and are designed to validate functions in `src/`.

To run all tests:

```bash
pytest tests/
```

To run a specific test file:

```bash
pytest tests/test_evaluate_model.py
```

Make sure you are in the project environment (conda or Docker) before running tests.
 

## Data validation

The project uses `src/data_validation.py` to perform automated data quality checks throughout the analysis pipeline. These checks run inside `source/02_data_cleaning.py` and `source/04_model_output.py`, so users do not need to execute the validation module directly.

The checks include validation of file format, expected columns, missingness, value ranges, category levels, boolean-like fields, class labels, and train/test split integrity. Most validation failures stop the pipeline and return an informative error. Duplicate observations are treated as a recoverable issue: they are flagged and removed during the cleaning step.

To run the pipeline with validation:

```bash
make all
```

or ran individually:

```bash
PYTHONPATH=. python source/02_data_cleaning.py data/raw_online_shoppers.csv data/processed_online_shoppers.csv
PYTHONPATH=. python source/04_model_output.py data/processed_online_shoppers.csv results/online_shoppers_model
```

# License
The software code in this project is licensed under the **MIT License**. 

The written analysis and reports in this project are included under the same repository and are also covered by the MIT License unless otherwise specified.

See [LICENSE](./LICENSE) for full details.