#!/usr/bin/env python3
"""
Rock Paper Scissors - Juego simple en la consola (español)

El usuario selecciona 1..3 y juega contra la CPU que selecciona al azar.
Incluye un modo demo (--demo) que ejecuta una partida no interactiva para pruebas.

Cómo usar (Windows PowerShell):
  python .\RockPaperScissors.py       # modo interactivo
  python .\RockPaperScissors.py --demo  # ejecuta una ronda de ejemplo

"""
import random
import sys


CHOICES = {
    "1": "Piedra",
    "2": "Papel",
    "3": "Tijeras",
}


def determine_winner(player_choice: str, cpu_choice: str) -> str:
    """Determina el resultado a partir de las opciones (valores: 'Piedra','Papel','Tijeras').

    Retorna 'empate', 'jugador' o 'cpu'.
    """
    if player_choice == cpu_choice:
        return "empate"

    wins = {
        ("Piedra", "Tijeras"),
        ("Tijeras", "Papel"),
        ("Papel", "Piedra"),
    }

    if (player_choice, cpu_choice) in wins:
        return "jugador"
    return "cpu"


def prompt_player() -> str:
    """Pide al usuario que elija 1-3 y devuelve la cadena correspondiente.
    Reintenta hasta recibir una entrada válida.
    """
    prompt = (
        "Elige una opción (escribe el número):\n"
        "  1) Piedra\n"
        "  2) Papel\n"
        "  3) Tijeras\n"
        "Tu elección: "
    )

    while True:
        choice = input(prompt).strip()
        if choice in CHOICES:
            return CHOICES[choice]
        print("Entrada inválida. Por favor, introduce 1, 2 o 3.\n")


def play_round(player_choice: str = None, demo: bool = False) -> None:
    """Juega una ronda. Si player_choice es None, pide al usuario la elección.
    Si demo=True, se imprime información adicional para pruebas.
    """
    if player_choice is None:
        player = prompt_player()
    else:
        player = player_choice

    cpu = CHOICES[str(random.randint(1, 3))]

    print("\nResultados:")
    print(f"  Tú elegiste: {player}")
    print(f"  CPU eligió: {cpu}\n")

    winner = determine_winner(player, cpu)
    if winner == "empate":
        print("Empate!")
    elif winner == "jugador":
        print("¡Has ganado!")
    else:
        print("La CPU ha ganado.")


def demo_run() -> None:
    """Ejecuta una ronda de demostración no interactiva (elige aleatoriamente el jugador)."""
    player = CHOICES[str(random.randint(1, 3))]
    print("Modo demo: generando una partida de ejemplo...\n")
    play_round(player_choice=player, demo=True)


def main(argv=None):
    argv = argv or sys.argv[1:]

    if "--demo" in argv:
        demo_run()
        return 0

    try:
        play_round()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
