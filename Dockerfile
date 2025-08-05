FROM python:3.12

RUN pip install --upgrade pip

RUN addgroup admin && adduser admin --ingroup admin

RUN chown -R admin:admin /home/admin/

USER admin

COPY --chown=admin:admin ./app /home/admin/app

ENV PATH="/home/admin/.local/bin:${PATH}"

RUN pip install -r /home/admin/app/requirements.pip

WORKDIR /home/admin/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--limit-concurrency", "300"]
