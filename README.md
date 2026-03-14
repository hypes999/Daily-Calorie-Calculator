# Daily Calorie Calculator

Uma aplicação web desenvolvida em Python com Streamlit para calcular a Taxa Metabólica Basal (BMR), o Gasto Energético Diário Total (TDEE) e as necessidades calóricas e de macronutrientes com base em objetivos de composição corporal.

Esta ferramenta foi desenhada com um foco em precisão científica e utilidade prática para nutricionistas, treinadores e entusiastas do fitness.

## Características Principais

- **Cálculo de BMR (Taxa Metabólica Basal)**: Utiliza a equação de Mifflin-St Jeor, amplamente reconhecida pela sua precisão.
- **Cálculo de TDEE (Gasto Energético Diário Total)**: Aplica fatores de atividade baseados no perfil semanal do utilizador.
- **Ajuste de Objetivos**:
    - Manutenção de Peso (TDEE).
    - Ganho de Massa (Lean Bulk): TDEE + 150 a 300 kcal.
    - Perda de Gordura (Fat Loss): TDEE - 300 a 500 kcal.
- **Arredondamento Científico**: Todos os valores calóricos são arredondados para os 10 kcal mais próximos, refletindo a precisão prática nutricional.
- **Gestão de Macronutrientes**:
    - **Modo Recomendado**: Baseado em evidência científica (Proteína: 2.0g/kg, Gordura: 0.8g/kg, Hidratos: restante).
    - **Modo Personalizado**: Permite ao utilizador definir as suas próprias percentagens de distribuição.
- **Interface Limpa e Profissional**: UI minimalista e responsiva, sem distrações visuais (emojis), focada na clareza dos dados.
- **Recálculo Dinâmico**: Todos os valores atualizam-se instantaneamente conforme os inputs mudam.

## Estrutura do Projeto

O código está organizado de forma modular para facilitar a manutenção e expansão:

- `app.py`: Lógica da interface Streamlit e fluxo da aplicação.
- `calculation.py`: Fórmulas matemáticas e lógica de cálculo de calorias e macros.
- `utils.py`: Dados auxiliares, como descrições de níveis de atividade e opções de objetivos.
- `requirements.txt`: Lista de dependências necessárias.

## Requisitos

- Python 3.8+
- Streamlit

## Instalação e Execução

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/teu-utilizador/calculadora-calorias-diarias.git
   cd calculadora-calorias-diarias
   ```

2. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar a aplicação**:
   ```bash
   streamlit run app.py
   ```

## Notas Científicas

- **Equação de BMR (Mifflin-St Jeor)**:
    - Homens: BMR = (10 × peso) + (6.25 × altura) − (5 × idade) + 5
    - Mulheres: BMR = (10 × peso) + (6.25 × altura) − (5 × idade) − 161
- **Fatores de Atividade**: Variam entre 1.45 e 1.90 dependendo da carga de treino e atividade diária (NEAT).
- **Aviso**: As necessidades calóricas são estimativas. O acompanhamento da tendência do peso corporal ao longo do tempo é essencial para validar a ingestão calórica real.

## Licença

Este projeto está licenciado sob a licença MIT - veja o ficheiro LICENSE para mais detalhes.
