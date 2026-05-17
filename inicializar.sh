#!/bin/sh
echo "=== 1. Atualizando o PIP ==="
pip install --upgrade pip

echo "=== 2. Instalando bibliotecas do site ==="
pip install streamlit pandas

echo "=== 3. Inicializando o Streamlit ==="
streamlit run /dados/app.py --server.port=8501 --server.address=0.0.0.0