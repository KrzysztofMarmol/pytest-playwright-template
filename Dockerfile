FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy


WORKDIR /automation


COPY requirements.txt .

# Note: pytest-playwright is already included in the base image, but specifying
# it in requirements.txt is good practice for local development consistency.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Command to run pytest
CMD ["pytest"] 