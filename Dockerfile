FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y python3 python3-pip

COPY . ./

RUN pip install pipenv
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

# You can overwrite command in `serverless.yml` template
CMD ["app.handler"]
