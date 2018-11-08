FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html
RUN pip install fastai

RUN pip install starlette uvicorn python-multipart aiohttp

ADD furniture-weights.pth furniture-weights.pth

ADD furniture.py furniture.py

# Run to trigger resnet download
RUN python furniture.py

EXPOSE 8008

# Start the server
CMD ["python", "furniture.py", "serve"]
