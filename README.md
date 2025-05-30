# Dwarf World Project v0.0000

## Decision table:
- This table contains all the possible technologies to be used in the project. I still have to decide which one I will use.

| Fase                                | Biblioteca / Tecnologia      | Prós                                                                                          | Contras                                                                                              | Wayland (via XWayland)          |
| ----------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------- |
| **1. Janela flutuante**             | **PySide6 / PyQt6**          | • Controle completo de janela (borda-free, translucidez real)<br>• Timers e animações nativos | • Heavyweight (➕60 MB Qt)<br>• LGPL/commercial                                                       | Nativo Qt6 / XWayland           |
|                                     | **PyGObject (GTK4 + Cairo)** | • Mais leve que Qt<br>• Transparência RGBA com Cairo<br>• Integra bem ao Wayland              | • Precisa configurar visual RGBA manualmente<br>• Menos exemplos de animação “out-of-box”            | Nativo GTK4 / XWayland          |
|                                     | **SDL2 / Pygame-CE**         | • Loop de jogo e gestão de janela simplificados<br>• Fácil carregar sprites e alpha           | • Controle de janela limitado (flags SDL)<br>• Precisa `SDL_VIDEODRIVER=wayland` ou cair em XWayland | Wayland experimental / XWayland |
| **2. Mundo procedural (protótipo)** | **Pymunk (Chipmunk2D)**      | • API Pythonic para corpos e colisões 2D<br>• Rápido para protótipo de física básica          | • Talvez overkill se só usar poucos cálculos simples                                                 | Roda junto, independente de GUI |
|                                     | **Lógica manual + random**   | • Total flexibilidade<br>• Sem dependências extra                                             | • Código “do zero” exige mais tempo<br>• Sem colisões automáticas                                    | Independente                    |
|                                     | **noise (Perlin/Simplex)**   | • Geração rápida de padrões 2D (terreno, nuvens)<br>• Fácil de usar                           | • Só gera ruído — não há sistema de física ou entidades                                              | Independente                    |
| **3. Mundo procedural (final)**     | **Pymunk + noise**           | • Combina física realista com geração de terreno/eventos aleatórios                           | • Depende de duas libs — curva de aprendizado maior                                                  | Independente                    |
|                                     | **PyBox2D**                  | • Motor de física mais completo (Box2D)                                                       | • Bindings em C++ podem complicar instalação                                                         | Independente                    |
| **4. Companion (protótipo)**        | **Pygame-CE**                | • Desenha formas simples (círculo/blob) fácil<br>• Loop integrado com o mundo                 | • A integração janela+física precisa “colar” código manualmente                                      | Wayland experimental / XWayland |
|                                     | **Qt Graphics View**         | • Cena 2D com itens (QGraphicsScene/QGraphicsItem)<br>• Animações e colisões básicas          | • Mais complexo de aprender que Pygame                                                               | Nativo Qt6 / XWayland           |
| **5. Companion (final)**            | **Pymunk + Pygame-CE / Qt**  | • Usa física para comportamentos (gravidade, colisões)<br>• Sprites animados frame-a-frame    | • Integração completa exige bom gerenciamento de loop e sincronismo                                  | Conforme GUI escolhida          |
| **Pixel Art & Rendering**           | **Pyxel**                    | • Ferramentas built-in para pixel art retro<br>• API muito simples                            | • Resolução e paleta limitadas (16 cores)                                                            | XWayland                        |
|                                     | **Cairo / QPainter**         | • Desenho vetorial e bitmap com alpha real<br>• Escalamento “pixel-per-pixel”                 | • Mais código “baixo nível” para cada frame                                                          | Nativo (GTK4/Cairo ou Qt)       |


## 1. Floating Window
- I decided to use the first option, the **PySide6**.
- I chose PySide6 because of its permissive license.
