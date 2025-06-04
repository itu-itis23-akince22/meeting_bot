FROM python:3.10.14-slim-bullseye

# Sistem paketlerini güncelle ve eksik kaynakları al
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    wget \
    unzip \
    xvfb \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libindicator7 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Chrome indir
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb

# ChromeDriver yükle
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1) && \
    wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["xvfb-run", "-a", "python", "join_google_meet.py"]
