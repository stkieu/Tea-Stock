FROM public.ecr.aws/lambda/python:3.13 as base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY AWS_Lambda/ ${LAMBDA_TASK_ROOT}/AWS_Lambda/


FROM base as lambda_scrape
COPY common/ ${LAMBDA_TASK_ROOT}/common/
COPY Scrapers/ ${LAMBDA_TASK_ROOT}/lambda_scrape/
COPY Dict/ ${LAMBDA_TASK_ROOT}/Dict/
CMD [ "AWS_Lambda.lambda.lambda_handler" ]

FROM base as lambda_discord
COPY lambdaDisc/ ${LAMBDA_TASK_ROOT}/lambdaDisc/
CMD [ "AWS_Lambda.lambdaDisc.lambda_handler" ]