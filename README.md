# Pipeline de Big Data Distribuído e Orquestração de Containers para Análise de Resíduos Sólidos

Este projeto implementa um pipeline de dados de ponta a ponta para processar e visualizar o Diagnóstico de Resíduos Sólidos Urbanos do Brasil. A arquitetura foi desenhada para simular um ambiente real de produção em nuvem utilizando processamento distribuído e orquestração de microsserviços.

## 🛠️ Tecnologias Utilizadas

* **Orquestração:** Kubernetes (via Kind)
* **Motor de Containers:** Podman (arquitetura segura e estável *daemonless*)
* **Processamento de Big Data:** Apache Spark (via Spark-on-K8s Operator)
* **Visualização Analítica:** Streamlit & Python 3.11
* **Armazenamento:** Volumes Persistentes do Kubernetes (PV/PVC)

## 🏗️ Arquitetura do Ecossistema

1. **Ingestão e Limpeza:** O Apache Spark processou uma base bruta de **43 MB e +119.000 linhas**, executando transformações paralelas e reduzindo o output para **1.1 MB** otimizados.
2. **Persistência Compartilhada:** Os dados tratados foram gravados em um volume compartilhado (`PersistentVolumeClaim`), permitindo comunicação segura entre diferentes Pods.
3. **Consumo Analítico:** Um Pod Python isolado executa o Streamlit para ler os dados processados e renderizar gráficos interativos sob demanda com baixíssima latência.

## 🧠 Desafios de Engenharia & Resolução de Problemas (Troubleshooting)

* **Controle de Acesso (RBAC):** Configuração de `ServiceAccount` e `ClusterRoleBinding` para dar autonomia ao Spark Driver para gerenciar os Pods executores.
* **Compatibilidade Linux/Windows:** Correção de quebras de linha de scripts ocultos de `CRLF` para `LF` para execução nativa dentro dos containers.
* **Ajuste de Caminhos e Redes:** Correção de rotas de volumes e portas de escuta (`0.0.0.0`) para viabilizar o `Port-Forward` seguro do cluster para a máquina local.