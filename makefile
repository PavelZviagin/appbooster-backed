test:
	pytest -p no:warnings

run:
	uvicorn main:app --reload