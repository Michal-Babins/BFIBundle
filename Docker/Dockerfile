FROM python:3.9 

Label software="bfibundle"
LABEL software.version="0.1/0"
LABEL maintainer="Michal Babinski"
LABEL maintainer.email="mbabinski@lanl.gov"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir bfibundle

CMD ["/bin/bash"]
