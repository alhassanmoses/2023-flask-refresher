FROM python:3.10
# EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir  --upgrade -r requirements.txt
RUN pip install flask
COPY . .
CMD [ "gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
# docker build -t [flask-rest-apis] [.]
# ================tag name===============================
# ==================================directory to locate dockerfile in===============================

# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-rest-apis
# ==============port used in browser===============================
# ===================port exposed within server/app===============================


# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" [IMAGE_NAME] sh -c "flask run"