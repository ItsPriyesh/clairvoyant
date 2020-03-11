FROM codait/max-base:v1.3.2

ARG model_file=assets.tar.gz

WORKDIR /workspace

COPY ${model_file} /workspace
RUN tar -x -C . -f ${model_file} -v && rm ${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

EXPOSE 5000

CMD python app.py
