FROM python:3-alpine

WORKDIR /usr/src/fum-counter-it

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd fum_counter_it

COPY . .

RUN chown -R secretary_manager /usr/src/fum-counter-it

USER fum_counter_it

ENV FLASK_ENV production

EXPOSE 5000

CMD ["sh", "start.sh"]

