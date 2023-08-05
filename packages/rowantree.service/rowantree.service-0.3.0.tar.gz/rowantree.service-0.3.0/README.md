# Rowan Tree Service

Overview
--------
The Rowan Tree Service Layer

Deployment
----------
**Start the service (development only):**
```
uvicorn src.rowantree.service.main:app --reload
```

**Production Deployment**

Create the docker container using the build script 'build.sh'.

Launch the container:
```
docker run -p 5000:80 --env API_DATABASE_SERVER='127.0.0.1' --env API_DATABASE_NAME='dev_trt' trt_client_api
```

Consumption
-----------
Default URL for API: `http(s)://{hostname}:8000/`
