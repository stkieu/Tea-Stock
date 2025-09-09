FROM public.ecr.aws/lambda/python:3.13

COPY FASTAPI/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY common/ ${LAMBDA_TASK_ROOT}/common/
COPY FASTAPI/ ${LAMBDA_TASK_ROOT}/FASTAPI
CMD [ "FASTAPI.main.handler" ]