# run pecu.cc api dev server

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload & cd front/client && npm run dev

# run pecu.cc react express server frontend

# cd front && npm start
