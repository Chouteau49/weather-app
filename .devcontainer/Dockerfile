FROM mcr.microsoft.com/devcontainers/python:3.11

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs

# Install Poetry
RUN pip install poetry

# Set workdir
WORKDIR /workspaces/poetry_python

EXPOSE 8000 5173