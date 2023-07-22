FROM python:3.11-alpine3.18 AS builder
WORKDIR /src
ADD . /src
RUN apk add build-base python3-dev && \
    pip install setuptools Cython && \
    python setup.py build_ext --build-lib compiled/lib && \
    cython --embed -o main.c main.py && \
    gcc -Os -I /usr/include/python3.11 main.c -lpython3.11 -o compiled/plexsync

FROM python:3.11-alpine3.18
WORKDIR /app
COPY --from=builder /src/compiled/lib/ /app/lib
COPY --from=builder /src/compiled/plexsync /app/plexsync
CMD /app/plexsync
