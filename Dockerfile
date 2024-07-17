FROM python:3.11

ADD 10min.py .

RUN pip install pandas tensorflow numpy matplotlib scikit-learn


CMD ["python", "./10min.py"]