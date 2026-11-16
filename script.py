import math
import random
import tkinter as tk
from tkinter import ttk

# ==============================================================================
# CONSTANTES EXIGIDAS PELO TRABALHO (LEVEL OF DETAIL - LoD)
# ==============================================================================
LIMITE_BAIXA = 10000
LIMITE_ALTA = 1000
LIMITE_PROCEDURAL = 200  # Abaixo de 200m ativa micro-detalhes arquitetônicos 3D
MINIMO_ALTITUDES = 5


def carregar_camada_satelite(lista_altitudes):
    """
    Função obrigatória do trabalho: recebe no mínimo 5 altitudes (metros)
    e classifica cada uma usando Level of Detail (LoD) 3D para ambientes urbanos.
    """
    if not isinstance(lista_altitudes, (list, tuple)):
        raise TypeError("A entrada deve ser uma lista ou tupla de altitudes.")
    if len(lista_altitudes) < MINIMO_ALTITUDES:
        raise ValueError(f"Informe no mínimo {MINIMO_ALTITUDES} altitudes.")

    camadas = []
    for altitude in lista_altitudes:
        if altitude < 0:
            raise ValueError(f"Altitude inválida: {altitude} m.")

        if altitude > LIMITE_BAIXA:
            nivel = "Baixa Resolução (LoD 0)"
            descricao = "Malha viária macro, zoneamento de quarteirões e massas volumétricas simples"
            ajuste_albedo = False
        elif altitude >= LIMITE_ALTA:
            nivel = "Média Resolução (LoD 1)"
            descricao = "Extrusão 3D de edifícios com sombreamento direcional e parques urbanos"
            ajuste_albedo = False
        else:
            nivel = "Alta Resolução (LoD 2/3)"
            descricao = "Detalhamento arquitetônico 3D: fachadas envidraçadas, helipontos, antenas e oclusão"
            ajuste_albedo = True

        camadas.append({
            "altitude_m": altitude,
            "nivel": nivel,
            "descricao": descricao,
            "ajuste_albedo": ajuste_albedo,
        })
        print(f"Altitude: {altitude:>7} m | {nivel} -> {descricao}")

    return camadas


class MotorCidade3D:
    """Gera uma metrópole 3D procedural com quarteirões, rio, parques e arranha-céus."""

    def __init__(self, semente=2026):
        self.rng = random.Random(semente)
        self.quarteiroes = []
        self.predios = []
        self._construir_metropole()

    def _construir_metropole(self):
        tamanho_bloco = 110
        largura_rua = 24
        passo = tamanho_bloco + largura_rua

        for gx in range(-5, 6):
            for gy in range(-5, 6):
                cx = gx * passo
                cy = gy * passo
                distancia_centro = math.hypot(gx, gy)

                if gx == 2:
                    self.quarteiroes.append({
                        "cx": cx, "cy": cy, "w": passo, "d": passo, "tipo": "agua"
                    })
                    continue

                if (gx == -1 and gy == 1) or (gx == 1 and gy == -2):
                    self.quarteiroes.append({
                        "cx": cx, "cy": cy, "w": tamanho_bloco, "d": tamanho_bloco, "tipo": "parque"
                    })
                    continue

                self.quarteiroes.append({
                    "cx": cx, "cy": cy, "w": tamanho_bloco, "d": tamanho_bloco, "tipo": "urbano"
                })

                if distancia_centro < 1.8:
                    qtd_predios = self.rng.randint(2, 3)
                    h_min, h_max = 150, 350
                elif distancia_centro < 3.6:
                    qtd_predios = self.rng.randint(3, 4)
                    h_min, h_max = 70, 195
                else:
                    qtd_predios = 4
                    h_min, h_max = 25, 85

                sub_w = tamanho_bloco / 2 - 6
                sub_d = tamanho_bloco / 2 - 6
                posicoes = [(-27, -27), (27, -27), (-27, 27), (27, 27)]
                self.rng.shuffle(posicoes)

                for i in range(qtd_predios):
                    ox, oy = posicoes[i]
                    px = cx + ox + self.rng.uniform(-4, 4)
                    py = cy + oy + self.rng.uniform(-4, 4)
                    w = sub_w * self.rng.uniform(0.78, 0.96)
                    d = sub_d * self.rng.uniform(0.78, 0.96)
                    h = self.rng.uniform(h_min, h_max)

                    estilo = self.rng.choice(["vidro", "concreto", "aco", "misto"])
                    if estilo == "vidro":
                        cor_topo, cor_f1, cor_f2 = "#6e8ca0", "#4a6b82", "#2e485b"
                    elif estilo == "concreto":
                        cor_topo, cor_f1, cor_f2 = "#b8bcc2", "#9499a1", "#686d75"
                    elif estilo == "aco":
                        cor_topo, cor_f1, cor_f2 = "#586069", "#3f464e", "#272c33"
                    else:
                        cor_topo, cor_f1, cor_f2 = "#a39e93", "#827d73", "#59554e"

                    self.predios.append({
                        "cx": px,
                        "cy": py,
                        "w": w,
                        "d": d,
                        "h": h,
                        "cor_topo": cor_topo,
                        "cor_f1": cor_f1,
                        "cor_f2": cor_f2,
                        "heliponto": h > 210 and self.rng.random() > 0.45,
                        "antena": h > 250 and self.rng.random() > 0.5,
                    })


class AbaCidade3D(tk.Frame):
    """Interface 3D interativa estilo Google Earth com Zoom, Tilt, Rotação e Pan."""

    def __init__(self, parent):
        super().__init__(parent, bg="#121212")
        self.largura_tela = 880
        self.altura_tela = 470
        self.cidade = MotorCidade3D(semente=2026)

        self.altitude = 2200
        self.fator_zoom = 1.0
        self.rotacao_graus = 35
        self.inclinacao_graus = 54
        self.pan_x = 0.0
        self.pan_y = 0.0
        self._mouse_rot = None
        self._mouse_pan = None

        self.canvas = tk.Canvas(
            self,
            width=self.largura_tela,
            height=self.altura_tela,
            bg="#0d1117",
            highlightthickness=1,
            highlightbackground="#2d333b",
        )
        self.canvas.pack(padx=15, pady=(10, 6))

        self.canvas.bind("<ButtonPress-1>", self._iniciar_rotacao)
        self.canvas.bind("<B1-Motion>", self._arrastar_rotacao)
        self.canvas.bind("<ButtonPress-3>", self._iniciar_pan)
        self.canvas.bind("<B3-Motion>", self._arrastar_pan)
        self.canvas.bind("<MouseWheel>", self._on_scroll)
        self.canvas.bind("<Button-4>", lambda e: self.aplicar_zoom(1.18))
        self.canvas.bind("<Button-5>", lambda e: self.aplicar_zoom(0.85))

        hud_zoom = tk.Frame(self.canvas, bg="#161b22", bd=1, relief="solid")
        self.canvas.create_window(
            self.largura_tela - 26,
            self.altura_tela - 26,
            window=hud_zoom,
            anchor="se",
        )

        tk.Button(
            hud_zoom,
            text="+",
            command=lambda: self.aplicar_zoom(1.25),
            bg="#21262d",
            fg="white",
            activebackground="#007acc",
            activeforeground="white",
            bd=0,
            font=("Arial", 12, "bold"),
            width=3,
            cursor="hand2",
        ).pack(pady=(2, 1), padx=2)

        tk.Button(
            hud_zoom,
            text="-",
            command=lambda: self.aplicar_zoom(0.80),
            bg="#21262d",
            fg="white",
            activebackground="#007acc",
            activeforeground="white",
            bd=0,
            font=("Arial", 12, "bold"),
            width=3,
            cursor="hand2",
        ).pack(pady=1, padx=2)

        tk.Button(
            hud_zoom,
            text="R",
            command=self.resetar_camera,
            bg="#21262d",
            fg="#00d4ff",
            activebackground="#007acc",
            activeforeground="white",
            bd=0,
            font=("Arial", 10, "bold"),
            width=3,
            cursor="hand2",
        ).pack(pady=(1, 2), padx=2)

        self.lbl_status = tk.Label(
            self,
            text="",
            fg="white",
            bg="#1e1e1e",
            font=("Consolas", 10),
            justify="left",
            padx=15,
            pady=8,
            width=104,
        )
        self.lbl_status.pack(pady=4)

        painel_ctrl = tk.Frame(self, bg="#121212")
        painel_ctrl.pack(pady=4, fill="x", padx=25)

        f_alt = tk.Frame(painel_ctrl, bg="#121212")
        f_alt.pack(side="left", expand=True, fill="x", padx=6)
        tk.Label(f_alt, text="Altitude / Zoom (m):", fg="#00d4ff", bg="#121212", font=("Arial", 9, "bold")).pack(anchor="w")
        self.slider_alt = tk.Scale(
            f_alt,
            from_=80,
            to=25000,
            orient="horizontal",
            length=250,
            bg="#121212",
            fg="white",
            troughcolor="#2c2c2c",
            highlightthickness=0,
            command=self._atualizar_parametros,
        )
        self.slider_alt.set(2200)
        self.slider_alt.pack(fill="x")

        f_tilt = tk.Frame(painel_ctrl, bg="#121212")
        f_tilt.pack(side="left", expand=True, fill="x", padx=6)
        tk.Label(f_tilt, text="Inclinação 3D (Tilt):", fg="#00ff9d", bg="#121212", font=("Arial", 9, "bold")).pack(anchor="w")
        self.slider_tilt = tk.Scale(
            f_tilt,
            from_=0,
            to=68,
            orient="horizontal",
            length=220,
            bg="#121212",
            fg="white",
            troughcolor="#2c2c2c",
            highlightthickness=0,
            command=self._atualizar_parametros,
        )
        self.slider_tilt.set(54)
        self.slider_tilt.pack(fill="x")

        f_rot = tk.Frame(painel_ctrl, bg="#121212")
        f_rot.pack(side="left", expand=True, fill="x", padx=6)
        tk.Label(f_rot, text="Rotação Orbital (360°):", fg="#ffb84d", bg="#121212", font=("Arial", 9, "bold")).pack(anchor="w")
        self.slider_rot = tk.Scale(
            f_rot,
            from_=0,
            to=360,
            orient="horizontal",
            length=220,
            bg="#121212",
            fg="white",
            troughcolor="#2c2c2c",
            highlightthickness=0,
            command=self._atualizar_parametros,
        )
        self.slider_rot.set(35)
        self.slider_rot.pack(fill="x")

        self.renderizar_cena_3d()

    def aplicar_zoom(self, fator):
        alt_atual = self.slider_alt.get()
        nova_alt = int(max(80, min(25000, alt_atual / fator)))
        if nova_alt == alt_atual:
            nova_alt = alt_atual - 20 if fator > 1 else alt_atual + 20
            nova_alt = max(80, min(25000, nova_alt))
        self.slider_alt.set(nova_alt)

    def resetar_camera(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.slider_alt.set(2200)
        self.slider_tilt.set(54)
        self.slider_rot.set(35)

    def _on_scroll(self, event):
        if event.delta > 0:
            self.aplicar_zoom(1.18)
        else:
            self.aplicar_zoom(0.85)

    def _iniciar_rotacao(self, event):
        self._mouse_rot = event.x

    def _arrastar_rotacao(self, event):
        if self._mouse_rot is not None:
            dx = event.x - self._mouse_rot
            self._mouse_rot = event.x
            self.slider_rot.set(int((self.slider_rot.get() + dx * 0.5) % 360))

    def _iniciar_pan(self, event):
        self._mouse_pan = (event.x, event.y)

    def _arrastar_pan(self, event):
        if self._mouse_pan is not None:
            dx = event.x - self._mouse_pan[0]
            dy = event.y - self._mouse_pan[1]
            self._mouse_pan = (event.x, event.y)
            self.pan_x += dx
            self.pan_y += dy
            self.renderizar_cena_3d()

    def _atualizar_parametros(self, _=None):
        self.altitude = int(self.slider_alt.get())
        self.inclinacao_graus = int(self.slider_tilt.get())
        self.rotacao_graus = int(self.slider_rot.get())
        self.renderizar_cena_3d()

    def _projetar_3d(self, x, y, z, rad_rot, cos_tilt, sin_tilt, escala):
        rx = x * math.cos(rad_rot) - y * math.sin(rad_rot)
        ry = x * math.sin(rad_rot) + y * math.cos(rad_rot)

        sx = self.largura_tela / 2 + self.pan_x + rx * escala
        sy = self.altura_tela / 2 + self.pan_y + (ry * cos_tilt - z * sin_tilt) * escala
        return sx, sy, ry

    def renderizar_cena_3d(self):
        self.canvas.delete("cena")

        escala = 1600.0 / (self.altitude + 320.0)
        self.fator_zoom = round(escala / (1600.0 / (2200 + 320.0)), 2)

        rad_rot = math.radians(self.rotacao_graus)
        rad_tilt = math.radians(self.inclinacao_graus)
        cos_tilt = math.cos(rad_tilt)
        sin_tilt = math.sin(rad_tilt)

        if self.inclinacao_graus > 35:
            altura_ceu = int((self.inclinacao_graus - 35) * 3.8)
            self.canvas.create_rectangle(0, 0, self.largura_tela, altura_ceu, fill="#162238", outline="", tags="cena")

        lim = 760
        cantos = [(-lim, -lim), (lim, -lim), (lim, lim), (-lim, lim)]
        pts_base = []
        for cx, cy in cantos:
            sx, sy, _ = self._projetar_3d(cx, cy, 0, rad_rot, cos_tilt, sin_tilt, escala)
            pts_base.extend([sx, sy])
        self.canvas.create_polygon(pts_base, fill="#22262c", outline="#383e47", width=2, tags="cena")

        for q in self.cidade.quarteiroes:
            hw, hd = q["w"] / 2, q["d"] / 2
            verts = [
                (q["cx"] - hw, q["cy"] - hd),
                (q["cx"] + hw, q["cy"] - hd),
                (q["cx"] + hw, q["cy"] + hd),
                (q["cx"] - hw, q["cy"] + hd),
            ]
            pts = []
            for vx, vy in verts:
                sx, sy, _ = self._projetar_3d(vx, vy, 0, rad_rot, cos_tilt, sin_tilt, escala)
                pts.extend([sx, sy])

            if q["tipo"] == "agua":
                self.canvas.create_polygon(pts, fill="#153b5c", outline="#1c4e78", tags="cena")
            elif q["tipo"] == "parque":
                self.canvas.create_polygon(pts, fill="#264d32", outline="#366b46", tags="cena")
            else:
                self.canvas.create_polygon(pts, fill="#30363f", outline="#444c56", tags="cena")

        predios_ordenados = []
        for p in self.cidade.predios:
            _, _, prof = self._projetar_3d(p["cx"], p["cy"], 0, rad_rot, cos_tilt, sin_tilt, escala)
            predios_ordenados.append((prof, p))
        predios_ordenados.sort(key=lambda item: item[0])

        mostrar_janelas = self.altitude < 1600 and self.inclinacao_graus > 12
        mostrar_detalhes_topo = self.altitude < 3500

        for _, p in predios_ordenados:
            hw, hd, h = p["w"] / 2, p["d"] / 2, p["h"]

            base_3d = [
                (p["cx"] - hw, p["cy"] - hd, 0),
                (p["cx"] + hw, p["cy"] - hd, 0),
                (p["cx"] + hw, p["cy"] + hd, 0),
                (p["cx"] - hw, p["cy"] + hd, 0),
            ]
            topo_3d = [(x, y, h) for (x, y, _) in base_3d]

            b2d = [self._projetar_3d(x, y, z, rad_rot, cos_tilt, sin_tilt, escala) for (x, y, z) in base_3d]
            t2d = [self._projetar_3d(x, y, z, rad_rot, cos_tilt, sin_tilt, escala) for (x, y, z) in topo_3d]

            if self.altitude < 8000 and self.inclinacao_graus > 5:
                sombra = [
                    b2d[1][0], b2d[1][1],
                    b2d[2][0], b2d[2][1],
                    b2d[2][0] + h * 0.22 * escala, b2d[2][1] + h * 0.14 * escala,
                    b2d[1][0] + h * 0.22 * escala, b2d[1][1] + h * 0.14 * escala,
                ]
                self.canvas.create_polygon(sombra, fill="#14171c", outline="", tags="cena")

            if self.inclinacao_graus > 2:
                faces = [
                    (0, 1, p["cor_f1"]),
                    (1, 2, p["cor_f2"]),
                    (2, 3, p["cor_f1"]),
                    (3, 0, p["cor_f2"]),
                ]
                for i1, i2, cor_face in faces:
                    ax, ay = b2d[i1][0], b2d[i1][1]
                    bx, by = b2d[i2][0], b2d[i2][1]
                    tx, ty = t2d[i1][0], t2d[i1][1]
                    cross = (bx - ax) * (ty - ay) - (by - ay) * (tx - ax)
                    if cross > 0:
                        poly_face = [
                            b2d[i1][0], b2d[i1][1],
                            b2d[i2][0], b2d[i2][1],
                            t2d[i2][0], t2d[i2][1],
                            t2d[i1][0], t2d[i1][1],
                        ]
                        self.canvas.create_polygon(poly_face, fill=cor_face, outline="#1b2028", tags="cena")

                        if mostrar_janelas and h > 50:
                            andares = min(14, max(3, int(h // 22)))
                            for andar in range(1, andares):
                                f = andar / andares
                                lx1 = b2d[i1][0] + (t2d[i1][0] - b2d[i1][0]) * f
                                ly1 = b2d[i1][1] + (t2d[i1][1] - b2d[i1][1]) * f
                                lx2 = b2d[i2][0] + (t2d[i2][0] - b2d[i2][0]) * f
                                ly2 = b2d[i2][1] + (t2d[i2][1] - b2d[i2][1]) * f
                                self.canvas.create_line(lx1, ly1, lx2, ly2, fill="#9ecbff", width=1, tags="cena")

            poly_topo = [
                t2d[0][0], t2d[0][1],
                t2d[1][0], t2d[1][1],
                t2d[2][0], t2d[2][1],
                t2d[3][0], t2d[3][1],
            ]
            self.canvas.create_polygon(poly_topo, fill=p["cor_topo"], outline="#cfd8e3", tags="cena")

            if mostrar_detalhes_topo:
                tcx, tcy, _ = self._projetar_3d(p["cx"], p["cy"], h, rad_rot, cos_tilt, sin_tilt, escala)
                if p["heliponto"]:
                    r_heli = max(3, 9 * escala)
                    self.canvas.create_oval(
                        tcx - r_heli,
                        tcy - r_heli * cos_tilt,
                        tcx + r_heli,
                        tcy + r_heli * cos_tilt,
                        outline="#ffd166",
                        width=1.5,
                        tags="cena",
                    )
                if p["antena"] and self.inclinacao_graus > 15:
                    ax, ay, _ = self._projetar_3d(p["cx"], p["cy"], h + 38, rad_rot, cos_tilt, sin_tilt, escala)
                    self.canvas.create_line(tcx, tcy, ax, ay, fill="#ff595e", width=1.5, tags="cena")

        self._desenhar_bussola()
        self._atualizar_status()

    def _desenhar_bussola(self):
        bx, by, r = self.largura_tela - 45, 45, 24
        self.canvas.create_oval(bx - r, by - r, bx + r, by + r, fill="#161b22", outline="#58a6ff", width=1.5, tags="cena")
        ang_norte = math.radians(-self.rotacao_graus - 90)
        nx = bx + math.cos(ang_norte) * (r - 5)
        ny = by + math.sin(ang_norte) * (r - 5)
        self.canvas.create_line(bx, by, nx, ny, fill="#ff4d4d", width=2.5, tags="cena")
        self.canvas.create_text(nx, ny, text="N", fill="white", font=("Arial", 8, "bold"), tags="cena")

    def _atualizar_status(self):
        if self.altitude > LIMITE_BAIXA:
            nivel = "BAIXA RESOLUÇÃO — LoD 0 (> 10.000 m)"
            detalhe = "Malha metropolitana global e massas volumétricas simplificadas"
        elif self.altitude >= LIMITE_ALTA:
            nivel = "MÉDIA RESOLUÇÃO — LoD 1 (1.000 m a 10.000 m)"
            detalhe = "Extrusão 3D de arranha-céus, sombras projetadas e zoneamento urbano"
        elif self.altitude >= LIMITE_PROCEDURAL:
            nivel = "ALTA RESOLUÇÃO 3D — LoD 2 (200 m a 1.000 m)"
            detalhe = "Fachadas envidraçadas, helipontos, antenas e oclusão dinâmica"
        else:
            nivel = "MICRO-ESCALA ARQUITETÔNICA — LoD 3 (< 200 m)"
            detalhe = "Zoom máximo 3D: detalhamento de andares e cânion urbano"

        modo_visao = "Nadir 2D (Satélite)" if self.inclinacao_graus < 10 else f"Perspectiva 3D ({self.inclinacao_graus}° Tilt)"
        self.lbl_status.config(
            text=f"ZOOM: {self.fator_zoom:.2f}x  |  ALTITUDE: {self.altitude} m  |  {nivel}\n"
                 f"CÂMERA: {modo_visao}  |  ROTAÇÃO: {self.rotacao_graus}°  (Scroll = Zoom | Esq = Girar | Dir = Mover)\n"
                 f"RENDERIZAÇÃO: {detalhe}"
        )


class MiniGoogleEarthApp:
    """Janela principal do simulador 3D."""

    def __init__(self, root):
        self.root = root
        self.root.title("TerraVision vs. Google Earth — Motor 3D Urbano (LoD + Zoom)")
        self.root.configure(bg="#121212")

        tk.Label(
            root,
            text="SIMULADOR 3D DE MAPEAMENTO URBANO E METRÓPOLES (GOOGLE EARTH 3D BUILDINGS)",
            fg="#00d4ff",
            bg="#121212",
            font=("Arial", 12, "bold"),
            pady=8,
        ).pack()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#121212", borderwidth=0)
        style.configure("TNotebook.Tab", background="#252526", foreground="white", padding=[18, 6], font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#007acc")], foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        aba_3d = AbaCidade3D(self.notebook)
        self.notebook.add(aba_3d, text="  Metrópole 3D Interativa (Zoom & 3D)  ")

        root.bind("<plus>", lambda e: aba_3d.aplicar_zoom(1.20))
        root.bind("<equal>", lambda e: aba_3d.aplicar_zoom(1.20))
        root.bind("<minus>", lambda e: aba_3d.aplicar_zoom(0.82))


if __name__ == "__main__":
    print("=== EXECUÇÃO DA FUNÇÃO OBRIGATÓRIA (LoD 3D URBANO) ===")
    carregar_camada_satelite([35000, 12000, 8500, 3200, 180])

    janela = tk.Tk()
    app = MiniGoogleEarthApp(janela)
    janela.mainloop()