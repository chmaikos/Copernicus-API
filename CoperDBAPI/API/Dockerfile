FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 5000

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libhdf5-dev libnetcdf-dev libudunits2-dev gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
