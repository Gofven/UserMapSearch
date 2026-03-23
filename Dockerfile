FROM continuumio/miniconda3

RUN mkdir /app
WORKDIR /app
COPY . /app/

# Setting up environment
RUN conda env create -f environment.yml
SHELL ["conda", "run", "--no-capture-output", "-n", "jobbtest", "/bin/bash", "-c"]

# Run Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "jobbtest", "python", "manage.py", "migrate"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "jobbtest", "python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
