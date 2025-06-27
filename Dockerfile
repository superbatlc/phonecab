# Builder stage - Install dependencies and build wheels
FROM python:3.8-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    make \
    musl-dev \
    linux-headers \
    # postgresql-dev \
    sqlite-dev \
    mariadb-dev \
    readline-dev \
    ncurses-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage - Lean production image
FROM python:3.8-alpine as runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /phonecab

# Install only runtime dependencies
RUN apk add --no-cache \
    # bash \
    # postgresql-dev \
    sqlite-dev \
    mariadb-connector-c \
    readline \
    ncurses \
    jpeg-dev \
    zlib-dev

# Copy python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the code (including entrypoint.py)
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh
# RUN python3 manage.py migrate

EXPOSE 8001

# Use relative path, since we're in /phonecab
ENTRYPOINT ["./entrypoint.sh"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]