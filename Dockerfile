FROM public.ecr.aws/lambda/python:3.13 as base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY AWS_Lambda/ ${LAMBDA_TASK_ROOT}/AWS_Lambda/


FROM base AS lambda_scrape
COPY common/ ${LAMBDA_TASK_ROOT}/common/
COPY Scrapers/ ${LAMBDA_TASK_ROOT}/Scrapers/
COPY Dict/ ${LAMBDA_TASK_ROOT}/Dict/
CMD [ "AWS_Lambda.lambda.lambda_handler" ]

FROM base AS lambda_discord
CMD [ "AWS_Lambda.lambdaDisc.lambda_handler" ]