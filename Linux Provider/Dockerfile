FROM python:3.9

# Install required packages
RUN apt-get update && apt-get install --no-install-recommends 
# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install jupyter nbconvert 

# Copy the application code
COPY lProvider.py providerUtils.py /app/
WORKDIR /app

# Run the application
CMD ["python", "lProvider.py"]