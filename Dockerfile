FROM python:3.11

ADD bitcoin_predictor.py .

RUN pip install pandas tensorflow numpy matplotlib scikit-learn


CMD ["python", "./bitcoin_predictor.py"]
