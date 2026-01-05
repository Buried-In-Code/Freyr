FROM python:3.14-slim

RUN apt-get update && apt-get install -y tzdata libpq5

WORKDIR /app

COPY freyr /app/freyr
COPY static /app/static
COPY templates /app/templates
COPY pyproject.toml README.md run.py /app/

RUN pip install --no-cache-dir .[postgres]

ENV TZ Pacific/Auckland
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV XDG_CACHE_HOME /app/cache
ENV XDG_CONFIG_HOME /app/config
RUN mkdir -p $XDG_CONFIG_HOME/freyr
ENV XDG_DATA_HOME /app/data
RUN mkdir -p $XDG_DATA_HOME/freyr

EXPOSE 25710

CMD ["python", "run.py"]
