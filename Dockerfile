# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install wkhtmltopdf
RUN apt-get update -y && \
    apt-get install -y wget xvfb libxrender1 fontconfig pandoc&& \
    wget --quiet https://downloads.wkhtmltopdf.org/0.12/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb || apt-get -y -f install && \
    apt-get install -y --no-install-recommends texlive-xetex texlive-fonts-recommended texlive-plain-generic&& \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME World

# Copy the app files into the container
COPY . /app

# Run the app when the container launches
CMD ["streamlit", "run", "notebook_to_pdf_app.py"]
