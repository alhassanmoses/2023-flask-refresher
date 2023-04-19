FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install flask
COPY . .
CMD [ "flask", "run", "--host", "0.0.0.0"]
# docker build -t [flask-rest-apis] [.]
# ================tag name===============================
# ==================================directory to locate dockerfile in===============================

# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-rest-apis
# ==============port used in browser===============================
# ===================port exposed within server/app===============================
