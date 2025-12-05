# Otimização em Transferência de Calor com Algoritmos Genéticos

Projeto acadêmico que utiliza **Algoritmos Genéticos (GA)** para resolver problemas clássicos de **transferência de calor**, com foco em visualização da otimização e compreensão do método.

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Casos de Uso](#casos-de-uso)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Resultados Esperados](#resultados-esperados)
- [Autores](#autores)

## 🔍 Sobre o Projeto

Este repositório contém implementações em Python que demonstram a aplicação de **Algoritmos Genéticos** a problemas de engenharia térmica. O projeto combina modelos físicos com otimização heurística, permitindo a busca automática de parâmetros ótimos respeitando restrições realistas.

### Principais Características

- ✅ Modelagem de problemas de transferência de calor
- ✅ Implementação de Algoritmos Genéticos com seleção, cruzamento e mutação
- ✅ Otimização multi-objetivo de parâmetros físicos
- ✅ Validação de restrições físicas e de regime (laminar/turbulento)
- ✅ Visualização gráfica da evolução do algoritmo
- ✅ Análise comparativa de gerações

## 🔧 Casos de Uso

### 1. Cilindro com Isolamento Térmico
**Objetivo:** Minimizar a espessura `t` do isolamento mantendo o fluxo de calor `Q` abaixo de um limite estabelecido.

**Parâmetros otimizados:**
- Espessura do isolamento (`t`)
- Condutividade térmica (`k`)
- Temperatura da parede (`T_w`)

### 2. Escoamento Laminar sobre Placa Plana
**Objetivo:** Calcular e otimizar a espessura da camada limite térmica `δ_t` sob diferentes condições de escoamento.

**Parâmetros otimizados:**
- Posição na placa (`x`)
- Número de Reynolds local (`Re_x`)
- Temperatura de parede (`T_w`)
- Propriedades do fluido

## 💻 Tecnologias

| Ferramenta | Descrição |
|-----------|-----------|
| **Python 3.x** | Linguagem principal |
| **NumPy** | Computação numérica e operações vetorizadas |
| **Matplotlib** | Visualização e plotagem de resultados |

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone ou baixe este repositório:
```bash
git clone <repository-url>
cd Evolutionary-AI-Implementation-Experiment
```

2. Instale as dependências:
```bash
pip install numpy matplotlib
```

## 🚀 Como Executar

### Executar simulação individual

```bash
python cilindro_ga.py
```

```bash
python placa_plana_ga.py
```

### Saída esperada

- **No terminal:** Valores otimizados dos parâmetros em cada geração
- **Janelas gráficas:** 
  - Evolução do fitness (melhor, média, pior)
  - Comportamento dos parâmetros físicos
  - Convergência do algoritmo

## 📁 Estrutura do Projeto

```
Evolutionary-AI-Implementation-Experiment/
│
├── cilindro_ga.py           # Otimização do cilindro com isolamento
├── placa_plana_ga.py        # Otimização de escoamento em placa plana
├── utils.py                 # Funções auxiliares (se existir)
├── README.md                # Este arquivo
└── resultados/              # Gráficos e dados gerados
```

## 📊 Resultados Esperados

### Gráficos Gerados

1. **Evolução do Fitness por Geração**
   - Linha superior: pior fitness
   - Linha média: fitness médio
   - Linha inferior: melhor fitness

2. **Comportamento de Parâmetros**
   - Evolução temporal de `t`, `k`, `Q`, `δ_t`
   - Convergência em relação ao ótimo

3. **Violação de Restrições**
   - Verificação de limites físicos respeitados

## 🎯 Objetivo Educacional

Este projeto demonstra:
- ✏️ Como acreçoer otimização numérica em engenharia
- ✏️ Comportamento e sintonia de Algoritmos Genéticos
- ✏️ Aplicação prática de computação evolucionária
- ✏️ Integração entre modelos físicos e otimização

## 📚 Referências

Para compreender melhor os conceitos utilizados:
- Algoritmos Genéticos: Holland (1975)
- Transferência de Calor: Incropera & DeWitt
- Dinâmica de Fluidos: White (2006)

## 👥 Autores

- **Pedro Belchior**
- **Enzo Moraes**
- **Antonio Neto**

---

*Última atualização: Dezembro de 2025*