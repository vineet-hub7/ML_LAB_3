FROM python:3.10

# Hugging Face Spaces require running as a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install them securely
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application files
COPY --chown=user . /app

# Expose port exactly to 7860 as required by Hugging Face
EXPOSE 7860

# Run the Flask app on host 0.0.0.0 and port 7860 via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
