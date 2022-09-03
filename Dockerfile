FROM python:3-slim

ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

COPY oddlots.py .

RUN pip install -r requirements.txt

HEALTHCHECK NONE

CMD ["python", "oddlots.py"]
