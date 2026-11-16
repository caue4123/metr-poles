# 🏙️ Análise Forense: TerraVision vs. Google Earth — Mapeamento Urbano e Metrópoles

> *"Como transformar milhões de dados geográficos brutos em uma cidade viva, interativa e em 3D na tela do computador?"*

Este projeto foi desenvolvido como parte da atividade prática de **Computação Gráfica & Ciência de Dados**[cite: 18, 19], inspirada na minissérie **Batalha Bilionária: O Caso Google Earth**[cite: 18, 19] — que retrata a histórica disputa de patente entre o coletivo alemão **ART+COM** (criador do *TerraVision*) e a **Google**[cite: 18, 19].

---

### 📋 Identificação do Projeto

* **Estudante:** Cauê de Mattos Amaral
* **Turma:** 3°D - Desenvolvimento de Sistemas (Matutino)[cite: 18]
* **Instituição:** Colégio Estadual Rodolpho Zaninelli[cite: 18]
* **Disciplinas:** Computação Gráfica & Ciência de Dados[cite: 18]
* **Professora:** Angélica Neckel[cite: 18, 19]
* **Tema Individual:** 1. Mapeamento Urbano e Metrópoles (Alta Densidade de Edificações)

---

### 📸 Referência Visual: O Desafio da Escala Urbana (Tóquio, Japão)

![Visão de Rua em Tóquio — Tokyo Sta. Chuoguchi](./tokyo-street-view.jpg)

A imagem acima (região central da Estação de Tóquio — *Tokyo Sta. Chuoguchi*) ilustra perfeitamente o maior desafio do mapeamento de grandes metrópoles: **a transição de escala e o efeito cânion urbano**[cite: 18, 20]. 

Quando olhamos uma metrópole do espaço, vemos apenas uma mancha cinza contínua. Porém, ao aproximarmos a câmera até o nível da rua, a geometria muda completamente: arranha-céus espelhados, sombras projetadas, fachadas com dezenas de andares, arborização viária e oclusão de prédios que ficam escondidos atrás de outros[cite: 20].

---

### 🧠 Conexão entre Ciência de Dados, Computação Gráfica e a Série

Durante o desenvolvimento do simulador em Python (`script.py`)[cite: 19], apliquei na prática os conceitos que foram o centro do julgamento mostrado na série[cite: 19]:

1. **Level of Detail (LoD) e Estruturas Condicionais (Episódios 2 e 4):**[cite: 18, 19]
   * No tribunal, a equipe alemã demonstrou que o segredo do *TerraVision* estava na lógica `if/else` que decidia quais dados carregar conforme a altitude da câmera[cite: 19].
   * No meu código, a função `carregar_camada_satelite()` e o motor 3D alternam automaticamente entre **LoD 0** (malha macro), **LoD 1** (extrusão volumétrica de edifícios) e **LoD 2/3** (janelas, helipontos e antenas em altitudes abaixo de 200 m).
2. **Projeção 3D, Sombreamento e Oclusão (Episódios 2 e 3):**[cite: 18, 19]
   * Para evitar que o computador travasse ao desenhar centenas de prédios simultaneamente, utilizei **Backface Culling** (desenha apenas as paredes viradas para a câmera) e o **Painter's Algorithm** (ordena os edifícios do mais distante para o mais próximo), garantindo que os arranha-céus da frente cubram corretamente os do fundo.
3. **Experiência do Usuário e Princípios de Gestalt (Episódios 1 e 2):**[cite: 18]
   * Assim como o *TerraVision* buscava uma navegação fluida e intuitiva[cite: 18], a interface permite explorar a cidade usando o **Scroll do mouse para Zoom**, **botão esquerdo para orbitar em 360°**, **botão direito para mover o mapa** e controle de **inclinação (Tilt)** entre a visão de satélite (2D) e a perspectiva urbana (3D).

---

### 🚀 Como Executar o Simulador

1. Certifique-se de ter o **Python 3** instalado no computador.
2. Baixe o arquivo `script.py`[cite: 19] deste repositório.
3. No terminal, execute:
   ```bash
   python script.py