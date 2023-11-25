FROM python:3.11

WORKDIR /app

COPY freyr /app/freyr
COPY static /app/static
COPY templates /app/templates
COPY pyproject.toml README.md run.py /app/

RUN pip install --no-cache-dir .[postgres]

ENV XDG_CACHE_HOME /app/cache
RUN mkdir -p $XDG_CACHE_HOME/freyr
ENV XDG_CONFIG_HOME /app/config
RUN mkdir -p $XDG_CONFIG_HOME/freyr
ENV XDG_DATA_HOME /app/data
RUN mkdir -p $XDG_DATA_HOME/freyr

EXPOSE 25710

CMD ["Freyr"]
