#! /bin/sh

echo "=================================================="
echo "            Instalando Python3"
echo "=================================================="
sudo apt-get install -y python3

echo "=================================================="
echo "            Instalamos Ice para Python"
echo "=================================================="
sudo apt-get install -y python-zeroc-ice36 python3-zeroc-ice zeroc-ice36

echo "=================================================="
echo "                Actualizando PIP"
echo "=================================================="
sudo -H pip3 install --upgrade pip

echo "=================================================="
echo "    Instalando librerias de python para networkx"
echo "=================================================="
sudo pip3 install networkx

echo "=================================================="
echo "    Instalando librerias de python para numpy"
echo "=================================================="
sudo pip3 install numpy

echo "=================================================="
echo "    Instalando librerias de python para scipy"
echo "=================================================="
sudo pip3 install scipy

echo "=================================================="
echo "    Instalando librerias de python para matplotlib"
echo "=================================================="
sudo pip3 install matplotlib

echo "=================================================="
echo "    Instalando librerias de python para lxml"
echo "=================================================="
sudo pip3 install lxml

echo "=================================================="
echo "    Instalando librerias de python para shapely"
echo "=================================================="
sudo pip3 install shapely

echo "=================================================="
echo "    Instalando librerias de python para nose"
echo "=================================================="
sudo pip3 install nose
