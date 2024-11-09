FROM python:3.9


RUN apt-get update && apt-get install --no-install-recommends 

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install jupyter nbconvert 


COPY lProvider.py providerUtils.py /app/
WORKDIR /app

CMD ["python", "lProvider.py"]