FROM python:3

ARG DEBIAN_FRONTEND=noninteractive

ARG QT_X11_NO_MITSHM=1
ARG QT_QPA_PLATFORM=offscreen
ARG QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins
ARG QT_QPA_FONTDIR=/usr/share/fonts
ARG QT_QPA_PLATFORMTHEME=qt5ct
ARG QT_STYLE_OVERRIDE=kvantum
ARG QT_AUTO_SCREEN_SCALE_FACTOR=1
ARG QT_SCALE_FACTOR=1
ARG QT_QPA_PLATFORM=wayland
ARG QT_WAYLAND_DISABLE_WINDOWDECORATION=1

ENV LIBGL_ALWAYS_INDIRECT=1

COPY / /app

WORKDIR /app

RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        python3-pyqt5 \
        python3-pyqt5.qtopengl \
        python3-pyqt5.qtquick \
        python3-pyqt5.qtmultimedia \
        qmlscene \
        qml-module-qtqml* \
        qml-module-qtquick* \
        qml-module-qmltermwidget \
        qml-module-qt-websockets \
        qml-module-qt3d \
        qml-module-qtaudioengine \
        qml-module-qtav \
        qml-module-qtbluetooth \
        qml-module-qtcharts \
        qml-module-qtdatavisualization \
        qml-module-qtgraphicaleffects \
        qml-module-qtgstreamer \
        qml-module-qtlocation \
        qml-module-qtmultimedia \
        qml-module-qtpositioning \
        libqt5multimedia5-plugins \
        gstreamer1.0-libav \
        gstreamer1.0-alsa \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-base-apps \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-ugly \
        alsa-utils

USER qtuser

RUN python -m pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt

CMD pip install --no-cache-dir -r requirements.txt; python main.py
