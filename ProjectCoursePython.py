from __future__ import annotations
import argparse
import string
import secrets
from random import SystemRandom
from typing import List

sr = SystemRandom()


def generate_password(length: int, groups: List[str]) -> str:
    """Genera una contraseña que incluye al menos un carácter de cada grupo proporcionado.

    length: longitud total de la contraseña
    groups: lista de strings; cada string es un conjunto de caracteres disponibles (por ejemplo, string.ascii_lowercase)
    """
    if length <= 0:
        raise ValueError("La longitud debe ser mayor que 0")
    if not groups:
        raise ValueError("Debe haber al menos un grupo de caracteres" )

    # Aseguramos que la contraseña contiene al menos un carácter de cada grupo seleccionado
    if length < len(groups):
        raise ValueError(f"La longitud ({length}) es menor que el número de grupos ({len(groups)}). Aumenta --length.")

    # Tomamos uno de cada grupo
    password_chars = [secrets.choice(g) for g in groups]
    remaining = length - len(password_chars)

    # Construimos el conjunto total de caracteres permitidos
    all_chars = ''.join(groups)
    password_chars += [secrets.choice(all_chars) for _ in range(remaining)]

    # Mezclamos de forma segura
    sr.shuffle(password_chars)

    return ''.join(password_chars)


def generate_passwords(count: int, length: int, use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool) -> List[str]:
    """Genera `count` contraseñas seguras con las opciones indicadas."""
    groups = []
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        # Limitamos algunos símbolos que pueden causar problemas en terminales, pero mantenemos variedad
        # Puedes cambiar a string.punctuation si prefieres todos los símbolos
        safe_symbols = "!#$%&()*+,-./:;?@[]^_{|}~"
        groups.append(safe_symbols)

    if not groups:
        raise ValueError("Has deshabilitado todos los tipos de caracteres. Activa al menos uno.")

    passwords = [generate_password(length, groups) for _ in range(count)]
    return passwords


def copy_to_clipboard(text: str) -> bool:
    """Copia `text` al portapapeles usando tkinter. Devuelve True si tuvo éxito."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # ahora el texto está en el portapapeles del sistema
        root.destroy()
        return True
    except Exception:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generador de contraseñas seguras")
    parser.add_argument('-l', '--length', type=int, default=12, help='Longitud de la contraseña (por defecto: 12)')
    parser.add_argument('-c', '--count', type=int, default=1, help='Cuántas contraseñas generar (por defecto: 1)')
    parser.add_argument('--no-uppercase', action='store_true', help='Excluir mayúsculas')
    parser.add_argument('--no-lowercase', action='store_true', help='Excluir minúsculas')
    parser.add_argument('--no-digits', action='store_true', help='Excluir dígitos')
    parser.add_argument('--no-symbols', action='store_true', help='Excluir símbolos')
    parser.add_argument('--copy', action='store_true', help='Copiar la primera contraseña al portapapeles (intenta usar tkinter)')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    use_upper = not args.no_uppercase
    use_lower = not args.no_lowercase
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    try:
        passwords = generate_passwords(args.count, args.length, use_upper, use_lower, use_digits, use_symbols)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Mostrar resultados
    print('\nGeneradas {n} contraseña(s):'.format(n=len(passwords)))
    for i, pw in enumerate(passwords, start=1):
        print(f"{i}. {pw}")

    if args.copy and passwords:
        ok = copy_to_clipboard(passwords[0])
        if ok:
            print('\nLa primera contraseña se copió al portapapeles.')
        else:
            print('\nNo se pudo copiar al portapapeles (posible falta de tkinter).')


if __name__ == '__main__':
    main()
