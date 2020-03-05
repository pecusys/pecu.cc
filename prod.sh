# prod run pecu.cc server

gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
