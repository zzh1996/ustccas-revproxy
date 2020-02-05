FROM python
RUN pip install flask
COPY auth_server.py /
ENV FLASK_APP auth_server.py
ENV FLASK_RUN_PORT 80
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]
