FROM python:3.10.5-slim-buster
 
# Create app directory
WORKDIR /generator
 
# Install app dependencies
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
# Bundle app source
COPY . .
RUN chmod a+x boot.sh

EXPOSE 8100

# # Fix for pyenchant -- needs C library 'enchant'
RUN apt update && apt install -y libenchant-dev
RUN pip install pyenchant


ENV FLASK_APP 'generator:create_app()'
CMD ["flask", "run", "--host", "0.0.0.0"]
ENTRYPOINT ["./boot.sh"]
