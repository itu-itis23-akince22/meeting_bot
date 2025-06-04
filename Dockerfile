FROM python:3.10.14-slim

# Sistem bağımlılıklarını kur
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    wget \
    unzip \
    xvfb \
    xauth \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libu2f-udev \
    fonts-liberation \
    portaudio19-dev \
    libportaudio2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Google Chrome (sabit sürüm)
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -f -y && \
    rm ./google-chrome-stable_current_amd64.deb

# ChromeDriver (Chrome 137.0.7151.69 için sabit sürüm)
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/137.0.7151.69/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Çalışma dizini
WORKDIR /app

# Dosyaları kopyala
COPY . /app

# Python bağımlılıklarını yükle
RUN pip install --upgrade pip && pip install -r requirements.txt

# Flask web servisini ve botu başlat
CMD ["python", "main.py"]

