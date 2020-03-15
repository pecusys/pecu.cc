# run pecu.cc api dev server

# uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload & cd front && npm run serve
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload & cd test && npm start

# run pecu.cc react express server frontend

# cd front && npm start
