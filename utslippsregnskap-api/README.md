### Utslippsregnskap-api service

To setup development with Conda, use following instructions:

1. `conda create -n <name> python=3.10`
2. `conda activate <name>`
3. `pip install -r ./requirements.txt`

To run the service in debug, run `DATA_PATH=<your-data-path> STORAGE_ACCOUNT=<your-storage-account> python app.py`.

To build an image and run the docker container locally:

1. `docker build --tag utslippsregnskap-api .`
2. `docker run -p 8000:8000 -e DATA_PATH=<your-data-path> -e STORAGE_ACCOUNT=<your-storage-account> utslippsregnskap-api`
