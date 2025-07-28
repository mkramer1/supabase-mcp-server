FROM python:3.12-slim-bookworm

WORKDIR /app

# Prepare the basic dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the current code
COPY . .

# Set a version for setuptools-scm to avoid build issues
ENV SETUPTOOLS_SCM_PRETEND_VERSION=1.0.0

# Install the package
RUN pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    pip install .

# Install additional dependencies for SSE transport
RUN pip install uvicorn sse-starlette

# Add pipx bin directory to PATH
ENV PATH="/root/.local/bin:$PATH"

# Start the server with SSE transport
ENTRYPOINT ["supabase-mcp-server"]
CMD ["--transport", "sse"]
