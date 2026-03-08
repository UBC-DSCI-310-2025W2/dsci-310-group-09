# dsci-310-group-09

## **To install the same env using conda-lock or docker**

### conda-lock

If you haven't used conda-lock before, you need to install it first:

`conda install -c conda-forge conda-lock`

Then create the environment using the conda-lock.yml file:

`conda-lock install -n online-shoppers conda-lock.yml`

Activate the new environment:

`conda activate online-shoppers`

### Dockerfile

First build a docker image:

`docker build -t online-shoppers .`

Second, run the docker container:

`docker run --rm -p 8888:8888 online-shoppers`

Finally, open browser and go to http://localhost:8888

The jupyter environment inside localhost8888 contain all dependencies needed to run the notebook.