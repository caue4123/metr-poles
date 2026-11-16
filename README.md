# 🏙️ Análise Forense: TerraVision vs. Google Earth — Mapeamento Urbano e Metrópoles

**Como transformar grandes volumes de dados geográficos em uma representação de cidade interativa e tridimensional?**

Este projeto surgiu de uma atividade prática das disciplinas de Computação Gráfica e Ciência de Dados. A proposta foi explorar como funciona o mapeamento de grandes cidades, tomando como referência a minissérie *Batalha Bilionária: O Caso Google Earth*.

A série apresenta a disputa entre a empresa alemã ART+COM, criadora do TerraVision, e a Google, envolvendo o desenvolvimento de tecnologias de visualização geográfica em 3D. A partir dessa história, desenvolvi um simulador em Python para trabalhar conceitos de representação urbana, modelagem tridimensional e navegação por mapas.

---

### 📋 Identificação do Projeto

- **Estudante:** Cauê de Mattos Amaral
- **Turma:** 3°D – Desenvolvimento de Sistemas (Matutino)
- **Instituição:** Colégio Estadual Rodolpho Zaninelli
- **Disciplinas:** Computação Gráfica e Ciência de Dados
- **Professora:** Angélica Neckel
- **Tema individual:** Mapeamento Urbano e Metrópoles (Alta Densidade de Edificações)

---

### 📸 Referência Visual: Mapeamento Urbano em Tóquio

A imagem abaixo mostra uma avenida na região central de Tóquio, próxima à Tokyo Station (Chuoguchi). Ela foi escolhida como referência porque apresenta características comuns de uma área metropolitana bastante adensada: edifícios altos, fachadas próximas umas das outras, vias movimentadas e árvores distribuídas pelas calçadas.

![Vista urbana de Tóquio, com edifícios altos e avenida](images/referencia-visual-toquio.png)

A imagem ajuda a visualizar o tipo de ambiente que o projeto procura representar. De longe, os edifícios formam um conjunto compacto. Quando observamos a região mais de perto, aparecem detalhes como janelas, fachadas, sombras, árvores, veículos e elementos da rua.

O desafio é representar essas estruturas em um ambiente tridimensional sem exigir processamento excessivo do computador. Também é preciso considerar a posição e o ângulo da câmera, já que os edifícios mais próximos podem esconder parte dos que estão atrás.

---

### 🧠 Relação entre Ciência de Dados, Computação Gráfica e TerraVision

Durante o desenvolvimento do simulador, utilizando Python no arquivo `script.py`, trabalhei com alguns conceitos apresentados na série e apliquei esses conhecimentos na construção do ambiente urbano.

**1. Level of Detail (LoD) e estruturas condicionais**

Um dos conceitos mais interessantes apresentados na disputa envolvendo o TerraVision é a escolha dos detalhes que aparecem conforme a câmera se aproxima ou se afasta do terreno.

No meu projeto, utilizei essa mesma ideia. O simulador trabalha com diferentes níveis de detalhamento:

- **LoD 0:** apresenta a estrutura geral do terreno e a malha urbana.
- **LoD 1:** adiciona volume às construções, representando os edifícios em 3D.
- **LoD 2/3:** acrescenta detalhes como janelas, helipontos e antenas quando a câmera chega a menos de 200 metros de altitude.

A função `carregar_camada_satelite()` participa desse processo, ajudando a controlar quais elementos aparecem em cada nível de aproximação.

**2. Projeção 3D, sombras e ocultação de edifícios**

Representar muitos prédios ao mesmo tempo pode exigir bastante do computador. Por isso, utilizei técnicas que ajudam a organizar a renderização e evitar cálculos desnecessários.

O **Backface Culling** elimina as faces dos objetos que não estão voltadas para a câmera. Já o **Painter's Algorithm** organiza os edifícios de acordo com a distância, desenhando primeiro os mais afastados e depois os mais próximos.

Isso permite representar melhor a profundidade da cidade e faz com que os prédios da frente escondam corretamente aqueles que estão atrás.

**3. Navegação e experiência do usuário**

Também procurei deixar a navegação simples, para que qualquer pessoa consiga explorar o ambiente sem precisar conhecer comandos complicados.

Os controles do simulador funcionam assim:

- **Scroll do mouse:** aproxima e afasta a câmera (Zoom).
- **Botão esquerdo:** permite girar a visualização em 360°.
- **Botão direito:** movimenta o mapa pela tela.
- **Controle Tilt:** altera a inclinação da câmera, permitindo alternar entre a visão de satélite em 2D e a perspectiva urbana em 3D.

A ideia é permitir que o usuário observe a cidade de diferentes ângulos e alturas, percebendo como a representação dos edifícios muda durante a navegação.

---

### 🚀 Como Executar o Simulador

Para testar o projeto, você precisa ter o Python 3 instalado no computador.

Depois, siga estes passos:

1. Baixe o arquivo `script.py` disponível neste repositório.
2. Abra o terminal na pasta onde o arquivo está salvo.
3. Execute o comando:

```bash
python script.py
```

Após a execução, o simulador será iniciado e você poderá explorar a representação urbana e testar os controles de navegação.
