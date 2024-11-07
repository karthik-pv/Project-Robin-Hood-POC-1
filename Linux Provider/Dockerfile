FROM ubuntu:latest

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    jupyter-notebook \
    jupyter-core \
    jupyter-client \
    jupyter-console \
    jupyter-nbconvert \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY lProvider.py providerUtils.py /app/
WORKDIR /app

# Run the application
CMD ["python", "lProvider.py"]