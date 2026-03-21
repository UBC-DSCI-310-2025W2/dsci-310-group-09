# dsci-310-group-09 — Online Shoppers Purchase Behavior Classification

This project builds classification models to predict whether an online shopping session results in a purchase, using the *Online Shoppers Purchasing Intention* dataset. We provide two fully reproducible ways to run the analysis: **conda-lock** (local environment) or **Docker** (containerized environment).

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

Open and run `notebooks/310-group9_online-shoppers-classification.ipynb` for full report.

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

Go to `localhost:8888` to access jupyter lab, and open `notebooks/310-group9_online-shoppers-classification.ipynb` for the full report.
