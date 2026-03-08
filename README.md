# dsci-310-group-09 Online Shoppers Purchase Behavior Classification Project

## **To install the same env using conda-lock or docker**

### conda-lock

If you haven't used conda-lock before, you need to install it first:

`conda install -c conda-forge conda-lock`

Then create the environment using the conda-lock.yml file:

`conda-lock install -n online-shoppers conda-lock.yml`

Activate the new environment:

`conda activate online-shoppers`

### Docker image

This project uses Docker to provide a reproducible computation environment. The Docker image is defined in the root-level `Dockerfile` and is automatically built and pushed to Docker Hub through GitHub Actions whenever the `Dockerfile` or dependency files are updated on `main`.

To pull the published image:

`docker pull yourdockerhubusername/dsci-310-group-09:latest`
