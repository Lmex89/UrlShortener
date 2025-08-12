# --------------------------------------------------------------------------------------
# Stage 1: Builder
# This stage installs Python dependencies into a dedicated directory.
# Using a separate stage keeps the final image smaller and more secure.
# --------------------------------------------------------------------------------------
FROM python:3.12 as builder

# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to the terminal without buffering.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group for security.
# Running as a non-root user is a critical security best practice.
RUN  pip install --upgrade pip

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory
WORKDIR /home/appuser/app

# Copy only the requirements file first to leverage Docker's build cache.
# This layer is only rebuilt if the requirements file changes.
COPY --chown=appuser:appgroup ./app/requirements.pip .

# Install dependencies into a specific directory within the user's home.
# Using --no-cache-dir keeps the layer size down.
# The --user flag installs packages for the current user, avoiding permission issues.
RUN pip install --no-cache-dir --user -r requirements.pip


# --------------------------------------------------------------------------------------
# Stage 2: Final Production Image
# This stage builds the final, lean image for runtime.
# --------------------------------------------------------------------------------------
FROM python:3.12-slim

# Set the same environment variables as the builder stage.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Recreate the same non-root user and set the working directory.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
WORKDIR /home/appuser/app

# Copy the installed Python packages from the builder stage.
# This is more efficient than reinstalling them.
COPY --from=builder --chown=appuser:appgroup /home/appuser/.local /home/appuser/.local

# Copy the application code. This is done last so that code changes
# don't invalidate the dependency installation cache layer.
COPY --chown=appuser:appgroup ./app .

# Add the user's local bin to the PATH. This allows us to run gunicorn directly.
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Expose the port the app will run on.
EXPOSE 9000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--limit-concurrency", "300"]
