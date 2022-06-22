FROM python:3.8

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "src/main.py", "-p", "path/to/program", "-t", "<generation/mutation>", "-i", "path/to/template", "-a", "'<fuzzed>'", "-e", "<extention>"]
