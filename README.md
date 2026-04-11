# dsci-310-group-09 — Online Shoppers Purchase Behavior Classification

This project builds classification models to predict whether an online shopping session results in a purchase, using the *Online Shoppers Purchasing Intention* dataset. We provide two fully reproducible ways to run the analysis: **conda-lock** (local environment) or **Docker** (containerized environment).

# Findings
Our findings showed that engagement related features were the most important predictors of online shopping behaviour. PageValue in particular, has the greatest influence on the model's performance followed by ExitRates, ProductRelated_Duration, ProductRelated, and BounceRates. According to the SHAP summary plot, high PageValue is associated with a positive SHAP value whereas high ExitRate is related to a negative SHAP value. This is not surprising as users who viewed high value pages are more likely to make a purchase compared to those who frequently exit pages. Longer viewing time of product related pages also indicate higher likelihood of purchase, in addition, users who leave the website quickly (High BounceRates) is related to lower purchase. The month of November is also found to positively relate with higher purchase, which is likely due to holiday shopping behaviour and sales occurring in this particular month. 

This suggests e-commerce businesses should prioritize the user’s website engagement by capitalizing on high value pages and improving website design to maximize product related duration, which can reduce bounce rates and increase the likelihood of a purchase. For instance, offering exclusive deals or customized recommendations on high value pages. Additionally, configuring UX/UI interface to improve functionality and ease of use to keep users on the website. 

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


# Notes on Container and Tests

## Stopping the Docker Container

When you are finished using the container, you can stop it in one of the following ways:

### 1. Stop directly in the terminal

If the container is running in your current terminal, simply press:

```bash
CTRL + C
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
Unit tests are located in the `tests/` directory and are designed to validate functions in `src/`.

To run all tests:

```bash
pytest tests/
```

To run a specific test file:

```bash
pytest tests/test_evaluate_model.py
```

Make sure you are in the project environment (conda or Docker) before running tests.
