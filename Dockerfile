FROM continuumio/miniconda3

# ---------- 1. Copy code & env spec ----------
WORKDIR /app
COPY conda_env.yaml .
RUN --mount=type=cache,target=/opt/conda/pkgs \
    conda env create -f conda_env.yaml

# ---------- 2. Set env name only once ----------
ARG CONDA_ENV=BaseCondaEnv         # keep one single source of truth
ENV PATH /opt/conda/envs/$CONDA_ENV/bin:$PATH \
    CONDA_DEFAULT_ENV=$CONDA_ENV

# optional: clean ~300 MB of package tarballs
RUN conda clean -afy

# ---------- 3. Copy the rest of the application ----------
COPY . .

# ---------- 4. Default command ----------
EXPOSE 8080
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
