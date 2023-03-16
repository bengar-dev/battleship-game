#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

# la grille de jeu virtuelle est composée de 10 x 10 cases
# une case est identifiée par ses coordonnées, un tuple (no_ligne, no_colonne)
# un no_ligne ou no_colonne est compris dans le programme entre 1 et 10,
# mais pour le joueur une colonne sera identifiée par une lettre (de 'A' à 'J')

TAILLE_GRILLE = 10

# détermination de la liste des lettres utilisées pour identifier les colonnes :
LETTRES = "ABCDEFGHIJ"

# chaque navire est constitué d'un dictionnaire dont les clés sont les
# coordonnées de chaque case le composant, et les valeurs correspondantes
# l'état de la partie du navire correspondant à la case
# (True : intact ; False : touché)

# les navires suivants sont disposés de façon fixe dans la grille :
#      +---+---+---+---+---+---+---+---+---+---+
#      | A | B | C | D | E | F | G | H | I | J |
#      +---+---+---+---+---+---+---+---+---+---+
#      | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|
# +----+---+---+---+---+---+---+---+---+---+---+
# |  1 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  2 |   | o | o | o | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  3 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  4 | o |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  5 | o |   | o |   |   |   |   | o | o | o |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  6 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  7 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  8 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  9 |   |   |   |   | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# | 10 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
porte_avion = {(2, 2): True, (2, 3): True, (2, 4)
                : True, (2, 5): True, (2, 6): True}
croiseur = {(4, 1): True, (5, 1): True, (6, 1): True, (7, 1): True}
contre_torpilleur = {(5, 3): True, (6, 3): True, (7, 3): True}
sous_marin = {(5, 8): True, (5, 9): True, (5, 10): True}
torpilleur = {(9, 5): True, (9, 6): True}
liste_navires = [porte_avion, croiseur,
                 contre_torpilleur, sous_marin, torpilleur]


def create_grid():
    """
    Returns
    ---
    grid: list"""

    grid = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(" ")
        grid.append(row)

    grid[1][1:6] = ["o"] * 5
    grid[3][0] = "o"
    grid[4][0] = "o"
    grid[5][0] = "o"
    grid[5][2] = "o"
    grid[5][8:11] = ["o"] * 3
    grid[7][0:3] = ["o"] * 3
    grid[9][4:6] = ["o"] * 2

    return grid


def print_grid(grid):
    """
    Param
    ----
    grid: list
    ----
    Returns
    ----
    void"""

    headers = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    print("   ".join(headers))
    print("+" + "---+" * len(grid[0]))
    for i, row in enumerate(grid):
        row_display = [str(i+1).rjust(2)] + row
        print("| " + " | ".join(row_display) + " |")
        print("+" + "---+" * len(grid[0]))


def navire_est_coule(navire):
    """
    Params
    ----
    navire: dict
    ----
    Returns
    ----
    bool"""
    if not True in navire.values():
        print("Le navire touché est coulé !")
        liste_navires.remove(navire)
        return True
    else:
        return False


def demande_coord(coord_joueur):
    """Param :
    ----
    coord_joueur: str
    ----
    Returns :
    ----
    Dict {
        coord_valides: bool,
        coord_tir: (int, int)
    }"""

    if 2 <= len(coord_joueur) <= 3:
        lettre, chiffre = coord_joueur[0], coord_joueur[1:]
        lettre = lettre.upper()
        try:
            no_lig = int(chiffre)
            no_col = ord(lettre) - ord('A') + 1
            if 1 <= no_lig <= TAILLE_GRILLE and lettre in LETTRES:
                return {
                    "coord_valides": True,
                    "coord_tir": (no_lig, no_col)
                }

        except ValueError:
            pass


def navire_est_touche(navire, coord_tir):
    """Param:
    ----
    navire: dict
    coord_tir: (number, number)
    grid: grille
    ----
    Returns
    ----
    bool"""
    if coord_tir in navire:
        if not navire[coord_tir]:
            print("Ce navire a déjà été touché !")
        if navire[coord_tir]:
            print("Un navire a été touché par votre tir !")
            navire[coord_tir] = False

        navire_est_coule(navire)

        return True

    else:
        print("Votre tir est tombé à l'eau")
        return False


start = True
grid = create_grid()


while liste_navires:
    coord_valides = False
    if start:
        print_grid(grid)
        start = False

    while not coord_valides:
        coord_joueur = input(
            "Entrez les coordonnées de votre tir (ex. : 'A1', 'H8') : ")

        coord_valides, coord_tir = demande_coord(
            coord_joueur)["coord_valides"], demande_coord(coord_joueur)["coord_tir"]

    for navire in liste_navires:
        shoot = navire_est_touche(navire, coord_tir)
        if shoot:
            grid[coord_tir[0] - 1][coord_tir[1] - 1] = "#"
            print_grid(grid)
            break
        else:
            grid[coord_tir[0] - 1][coord_tir[1] - 1] = "X"
            print_grid(grid)
            break


print('Bravo, vous avez coulé tous les navires')
