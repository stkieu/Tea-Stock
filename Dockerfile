FROM public.ecr.aws/lambda/python:3.13 as base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY AWS_Lambda/ ${LAMBDA_TASK_ROOT}/AWS_Lambda/
RUN pip install -r requirements.txt

FROM base as lambda_scrape
COPY common/ ${LAMBDA_TASK_ROOT}/common/
COPY lambda_scrape/ ${LAMBDA_TASK_ROOT}/lambda/
COPY Dict/ ${LAMBDA_TASK_ROOT}/Dict/
CMD [ "aws_lambda.lambda.lambda_handler" ]

FROM base as lambda_discord
COPY lambda_discord/ ${LAMBDA_TASK_ROOT}/lambdaDisc/
CMD [ "aws_lambda.lambda_discord.lambda_handler" ]

FROM base as lambda_API
COPY common/ ${LAMBDA_TASK_ROOT}/common/
COPY FASTAPI/ ${LAMBDA_TASK_ROOT}/FASTAPI/
CMD [ "main.handler" ]