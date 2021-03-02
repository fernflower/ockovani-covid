FROM python:3.7

WORKDIR /ockovani-covid
COPY requirements.txt ./
# create virtualenv & install requirements
RUN python3 -m venv venv3 && venv3/bin/pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["/ockovani-covid/entrypoint.sh"]
