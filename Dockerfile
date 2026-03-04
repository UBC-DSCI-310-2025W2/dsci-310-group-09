# Pin the base image version (important for reproducibility)
FROM quay.io/jupyter/scipy-notebook:2025-12-31

WORKDIR /home/jovyan/work

# Copy the project files
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/work

# Install extra packages not already in the base image
RUN pip install --no-cache-dir shap

EXPOSE 8888

CMD ["start-notebook.sh", "--NotebookApp.token=", "--NotebookApp.password="]
