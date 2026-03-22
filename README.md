# dsci-310-group-09 — Online Shoppers Purchase Behavior Classification

This project builds classification models to predict whether an online shopping session results in a purchase, using the *Online Shoppers Purchasing Intention* dataset. We provide two fully reproducible ways to run the analysis: **conda-lock** (local environment) or **Docker** (containerized environment).

# Findings
Our findings showed that engagement related features were the most important predictors of online shopping behaviour. PageValue in particular, has the greatest influence on the model's performance followed by ExitRates, ProductRelated_Duration, ProductRelated, and BounceRates. According to the SHAP summary plot, high PageValue is associated with a positive SHAP value whereas high ExitRate is related to a negative SHAP value. This is not surprising as users who viewed high value pages are more likely to make a purchase compared to those who frequently exit pages. Longer viewing time of product related pages also indicate higher likelihood of purchase, in addition, users who leave the website quickly (High BounceRates) is related to lower purchase. The month of November is also found to positively relate with higher purchase, which is likely due to holiday shopping behaviour and sales occurring in this particular month. 

This suggests e-commerce businesses should prioritize the user’s website engagement by capitalizing on high value pages and improving website design to maximize product related duration, which can reduce bounce rates and increase the likelihood of a purchase. For instance, offering exclusive deals or customized recommendations on high value pages. Additionally, configuring UX/UI interface to improve functionality and ease of use to keep users on the website. 

## Reproducibility and Dependencies

- **Conda environment (locked):** `conda-lock.yml`  
- **Container definition:** `Dockerfile`  
- **Automated image publishing:** GitHub Actions builds and pushes the Docker image to Docker Hub when the `Dockerfile` or dependency files are updated on `main`.

---

### Option A: Run with conda-lock (recommended for local development)

Install conda-lock, create environment and activate jupyter. Run the code below one line at a time.

```bash
conda install -c conda-forge conda-lock
conda-lock install -n online-shoppers conda-lock.yml
conda activate online-shoppers
jupyter lab
```

Open and run `analysis/310-group9_online-shoppers-classification.ipynb` for full report.

### Option B: Run using Docker

The Docker image is defined in the root-level Dockerfile and is automatically built and pushed to Docker Hub through GitHub Actions whenever the Dockerfile or dependency files are updated on main.

Pull the published image, run jupyter inside container:

```bash
docker pull cjz115/dsci-310-group-09:latest
```

Run container and start jupyter lab,

```bash
docker run --rm -it \
  -p 8888:8888 \
  -v "$PWD":/home/jovyan/work \
  -w /home/jovyan/work \
  cjz115/dsci-310-group-09:latest \
  jupyter lab --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
  ```

Go to `localhost:8888` to access jupyter lab, and open `analysis/310-group9_online-shoppers-classification.ipynb` for the full report.

