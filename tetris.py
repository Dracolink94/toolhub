import pygame
import random

# Configuration des blocs et de la grille
LARG, HAUT = 10, 20
TAILLE_CASE = 30
FEN_LARG = LARG * TAILLE_CASE
FEN_HAUT = HAUT * TAILLE_CASE

# Couleurs (RGB)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (40, 40, 40)
COULEURS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Bleu
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Jaune
    (0, 255, 0),    # Vert
    (128, 0, 128),  # Violet
    (255, 0, 0)     # Rouge
]

SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1], [1, 1]], # O
    [[0, 1, 1], [1, 1, 0]], # Z
    [[1, 1, 0], [0, 1, 1]]  # S
]

class Tetris:
    def __init__(self):
        self.grille = [[0] * LARG for _ in range(HAUT)]
        self.nouvelle_piece()
        self.score = 0
        self.game_over = False

    def nouvelle_piece(self):
        self.piece = random.choice(SHAPES)
        self.couleur = random.choice(COULEURS)
        self.px = LARG // 2 - len(self.piece[0]) // 2
        self.py = 0
        if self.collision(self.px, self.py, self.piece):
            self.game_over = True

    def collision(self, x, y, piece):
        for r, ligne in enumerate(piece):
            for c, val in enumerate(ligne):
                if val:
                    if x + c < 0 or x + c >= LARG or y + r >= HAUT:
                        return True
                    if self.grille[y + r][x + c]:
                        return True
        return False

    def figer_piece(self):
        for r, ligne in enumerate(self.piece):
            for c, val in enumerate(ligne):
                if val:
                    self.grille[self.py + r][self.px + c] = self.couleur
        self.supprimer_lignes()
        self.nouvelle_piece()

    def supprimer_lignes(self):
        lignes_a_garder = [l for l in self.grille if any(c == 0 for c in l)]
        lignes_supprimees = HAUT - len(lignes_a_garder)
        self.score += lignes_supprimees * 100
        self.grille = [[0] * LARG for _ in range(lignes_supprimees)] + lignes_a_garder

    def deplacer(self, dx, dy):
        if not self.collision(self.px + dx, self.py + dy, self.piece):
            self.px += dx
            self.py += dy
            return True
        if dy > 0:
            self.figer_piece()
        return False

    def tourner(self):
        piece_tournee = list(zip(*self.piece[::-1]))
        if not self.collision(self.px, self.py, piece_tournee):
            self.piece = piece_tournee

def main():
    print("[*] Initialisation de Pygame pour Tetris...")
    pygame.init()
    fenetre = pygame.display.set_mode((FEN_LARG, FEN_HAUT))
    pygame.display.set_caption("Tetris - Toolhub Edition")
    clock = pygame.time.Clock()
    
    jeu = Tetris()
    temps_chute = 0
    vitesse = 500 # Vitesse de chute en millisecondes
    
    continuer = True
    while continuer and not jeu.game_over:
        temps_chute += clock.get_rawtime()
        clock.tick()
        
        if temps_chute >= vitesse:
            jeu.deplacer(0, 1)
            temps_chute = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jeu.deplacer(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    jeu.deplacer(1, 0)
                elif event.key == pygame.K_DOWN:
                    jeu.deplacer(0, 1)
                elif event.key == pygame.K_UP:
                    jeu.tourner()

        # Dessin de l'écran
        fenetre.fill(NOIR)
        
        # Dessin de la grille fixe
        for r in range(HAUT):
            for c in range(LARG):
                if jeu.grille[r][c]:
                    pygame.draw.rect(fenetre, jeu.grille[r][c], (c*TAILLE_CASE, r*TAILLE_CASE, TAILLE_CASE-1, TAILLE_CASE-1))
                else:
                    pygame.draw.rect(fenetre, GRIS, (c*TAILLE_CASE, r*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

        # Dessin de la pièce active
        for r, ligne in enumerate(jeu.piece):
            for c, val in enumerate(ligne):
                if val:
                    pygame.draw.rect(fenetre, jeu.couleur, ((jeu.px + c)*TAILLE_CASE, (jeu.py + r)*TAILLE_CASE, TAILLE_CASE-1, TAILLE_CASE-1))

        pygame.display.flip()

    pygame.quit()
    print(f"\n[+] Partie terminée ! Score final : {jeu.score}")
    input("Appuie sur Entrée pour revenir au Toolhub...")

if __name__ == "__main__":
    main()
