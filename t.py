import tkinter as tk
import random

# ----- Configurações -----
GRID_SIZE = 10
CELL_SIZE = 60
VISION_RANGE = 1
TEMPO_ENTRE_PASSOS = 800  # ms

# Cores temáticas
COR_FUNDO = "#001f33"
COR_VISIVEL = "#0099cc"
COR_LIXO = "#555555"
COR_DRONE = "#ff3333"

# ----- Gerar dados do oceano -----
def gerar_dado_ponto():
    return {
        "temperatura": round(random.uniform(5, 30), 1),
        "ph": round(random.uniform(6.5, 8.5), 2),
        "lixo": random.choice([True, False, False, False])
    }

oceano = [[gerar_dado_ponto() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# ----- Classe principal -----
class DroneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌊 Visão Subaquática do Drone Ambiental")
        self.canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, bg=COR_FUNDO)
        self.canvas.pack(side=tk.LEFT)

        self.info_text = tk.Text(root, width=40, height=30, bg="#002b40", fg="white", font=("Courier", 10))
        self.info_text.pack(side=tk.RIGHT, padx=10, pady=10)
        self.info_text.insert(tk.END, "🔍 Iniciando monitoramento...\n")

        self.drone_pos = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
        self.root.after(1000, self.mover_drone)

    def desenhar_grade(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                dentro_visao = abs(i - self.drone_pos[0]) <= VISION_RANGE and abs(j - self.drone_pos[1]) <= VISION_RANGE
                dados = oceano[i][j]

                if dentro_visao:
                    cor = COR_VISIVEL
                    if dados["lixo"]:
                        cor = COR_LIXO
                else:
                    cor = COR_FUNDO

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="#00334d")

        # Desenhar o drone
        dx, dy = self.drone_pos
        x1 = dy * CELL_SIZE + 15
        y1 = dx * CELL_SIZE + 15
        x2 = x1 + CELL_SIZE - 30
        y2 = y1 + CELL_SIZE - 30
        self.canvas.create_oval(x1, y1, x2, y2, fill=COR_DRONE, outline="white", width=2)

    def mostrar_dados(self, dados):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"📍 Posição do Drone: {tuple(self.drone_pos)}\n\n")
        self.info_text.insert(tk.END, "📡 Dados coletados:\n")
        for (x, y, ponto) in dados:
            self.info_text.insert(tk.END, f"• ({x},{y}) Temp: {ponto['temperatura']}°C, "
                                          f"pH: {ponto['ph']}, Lixo: {'Sim' if ponto['lixo'] else 'Não'}\n")

    def coletar_dados_visao(self):
        dados = []
        x, y = self.drone_pos
        for dx in range(-VISION_RANGE, VISION_RANGE + 1):
            for dy in range(-VISION_RANGE, VISION_RANGE + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    dados.append((nx, ny, oceano[nx][ny]))
        return dados

    def mover_drone(self):
        # Movimento aleatório suave
        self.drone_pos[0] = max(0, min(GRID_SIZE - 1, self.drone_pos[0] + random.choice([-1, 0, 1])))
        self.drone_pos[1] = max(0, min(GRID_SIZE - 1, self.drone_pos[1] + random.choice([-1, 0, 1])))

        self.desenhar_grade()
        dados = self.coletar_dados_visao()
        self.mostrar_dados(dados)

        self.root.after(TEMPO_ENTRE_PASSOS, self.mover_drone)

# ----- Iniciar App -----
if __name__ == "__main__":
    root = tk.Tk()
    app = DroneApp(root)
    root.mainloop()

