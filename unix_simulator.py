#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Operativo Unix Simulado
Autor: Sistema de Simulación
"""

import os
import sys
from datetime import datetime

class Colors:
    """Clase para manejar colores en la terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class UnixSimulator:
    """Simulador de Sistema Operativo Unix"""
    
    def __init__(self):
        self.current_directory = "/"
        self.users = {
            "eth": "admin",
            "user": "guest",
            "root": "superuser"
        }
        self.current_user = "eth"
        self.hostname = "EthOS"
        
        # Sistema de archivos simulado con estructura jerárquica
        self.file_system = {
            "/": {"type": "dir", "contents": ["home", "bin", "etc", "var", "opt"]},
            "/home": {"type": "dir", "contents": ["eth", "user"]},
            "/home/eth": {"type": "dir", "contents": ["Documents", "Downloads", "secret.txt"]},
            "/home/eth/Documents": {"type": "dir", "contents": ["proyecto.py", "notas.txt"]},
            "/home/eth/Downloads": {"type": "dir", "contents": ["archivo.zip"]},
            "/home/user": {"type": "dir", "contents": ["file1.txt", "file2.txt"]},
            "/bin": {"type": "dir", "contents": ["ls", "cd", "pwd", "clear", "help", "exit", "whoami", "date"]},
            "/etc": {"type": "dir", "contents": ["config.conf", "passwd"]},
            "/var": {"type": "dir", "contents": ["log"]},
            "/var/log": {"type": "dir", "contents": ["system.log", "error.log"]},
            "/opt": {"type": "dir", "contents": ["apps", "tools"]}
        }
        
        self.history = []
        self.welcome_message()
    
    def welcome_message(self):
        """Muestra mensaje de bienvenida estilo hacker"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════╗")
        print("║         🔓 SISTEMA UNIX SIMULADO - ACCESO PERMITIDO   ║")
        print("║                     EthOS v2.0                        ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(f"{Colors.GREEN}[✓] Autenticación exitosa")
        print(f"[✓] Inicializando kernel...")
        print(f"[✓] Cargando sistema de archivos...")
        print(f"[✓] Acceso concedido - Bienvenido {self.current_user}@{self.hostname}")
        print(f"[!] Escribe 'help' para ver comandos disponibles{Colors.RESET}\n")
    
    def print_prompt(self):
        """Imprime el prompt personalizado"""
        prompt = f"{Colors.GREEN}{Colors.BOLD}{self.current_user}@{self.hostname}{Colors.CYAN}:{self.current_directory}{Colors.GREEN}${Colors.RESET} "
        return prompt
    
    def normalize_path(self, path):
        """Normaliza una ruta relativa a absoluta"""
        if path.startswith("/"):
            return path
        elif path == "~":
            return f"/home/{self.current_user}"
        elif path == "..":
            if self.current_directory == "/":
                return "/"
            return "/".join(self.current_directory.rstrip("/").split("/")[:-1]) or "/"
        elif path == ".":
            return self.current_directory
        else:
            if self.current_directory == "/":
                return "/" + path
            return self.current_directory.rstrip("/") + "/" + path
    
    def path_exists(self, path):
        """Verifica si una ruta existe"""
        return path in self.file_system
    
    def cmd_ls(self, args):
        """Comando: ls - Lista archivos y directorios"""
        path = self.normalize_path(args[0] if args else ".")
        
        if not self.path_exists(path):
            print(f"{Colors.RED}[✗] Error: No such file or directory: {path}{Colors.RESET}")
            return
        
        items = self.file_system[path]["contents"]
        
        if not items:
            return
        
        # Mostrar archivos con colores
        output = []
        for item in items:
            item_path = (path.rstrip("/") + "/" + item) if path != "/" else "/" + item
            if self.path_exists(item_path):
                if self.file_system[item_path]["type"] == "dir":
                    output.append(f"{Colors.BLUE}{Colors.BOLD}{item}/{Colors.RESET}")
                else:
                    output.append(f"{Colors.WHITE}{item}{Colors.RESET}")
        
        print("  ".join(output))
    
    def cmd_cd(self, args):
        """Comando: cd [directorio] - Cambiar de directorio"""
        if not args:
            # Sin argumentos, ir al home
            self.current_directory = f"/home/{self.current_user}"
            print(f"{Colors.GREEN}[✓] Acceso concedido{Colors.RESET}")
            return
        
        target = self.normalize_path(args[0])
        
        if not self.path_exists(target):
            print(f"{Colors.RED}[✗] Acceso denegado - Directorio no encontrado: {target}{Colors.RESET}")
            return
        
        if self.file_system[target]["type"] != "dir":
            print(f"{Colors.RED}[✗] Error: No es un directorio{Colors.RESET}")
            return
        
        self.current_directory = target
        print(f"{Colors.GREEN}[✓] Acceso concedido{Colors.RESET}")
    
    def cmd_pwd(self, args):
        """Comando: pwd - Muestra la ruta actual"""
        print(self.current_directory)
    
    def cmd_clear(self, args):
        """Comando: clear - Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cmd_help(self, args):
        """Comando: help - Muestra ayuda"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}COMANDOS DISPONIBLES - EthOS v2.0{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════{Colors.RESET}\n")
        
        commands = {
            "ls [path]": "Lista archivos y directorios",
            "cd [dir]": "Cambiar de directorio",
            "pwd": "Mostrar directorio actual",
            "clear": "Limpiar pantalla",
            "whoami": "Mostrar usuario actual",
            "date": "Mostrar fecha y hora",
            "cat [file]": "Mostrar contenido de archivo",
            "mkdir [dir]": "Crear directorio",
            "echo [text]": "Imprimir texto",
            "help": "Mostrar esta ayuda",
            "easter": "Activar modo secreto 🔐",
            "exit": "Salir del simulador"
        }
        
        for cmd, desc in commands.items():
            print(f"{Colors.GREEN}{cmd:20}{Colors.RESET} → {desc}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════{Colors.RESET}\n")
    
    def cmd_whoami(self, args):
        """Comando: whoami - Muestra el usuario actual"""
        print(f"{Colors.YELLOW}{self.current_user}{Colors.RESET}")
    
    def cmd_date(self, args):
        """Comando: date - Muestra fecha y hora"""
        current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        print(current_time)
    
    def cmd_cat(self, args):
        """Comando: cat [archivo] - Muestra contenido del archivo"""
        if not args:
            print(f"{Colors.RED}[✗] Error: Debes especificar un archivo{Colors.RESET}")
            return
        
        file_path = self.normalize_path(args[0])
        
        if not self.path_exists(file_path):
            print(f"{Colors.RED}[✗] Error: Archivo no encontrado: {file_path}{Colors.RESET}")
            return
        
        if self.file_system[file_path]["type"] != "file":
            print(f"{Colors.RED}[✗] Error: No es un archivo{Colors.RESET}")
            return
        
        # Contenidos simulados
        contents = {
            "/home/eth/secret.txt": f"{Colors.MAGENTA}┌─────────────────────────────┐\n│  SECRETO CLASIFICADO 🔐    │\n│  Acceso: Solo administrador │\n│  Nivel de seguridad: ALTO   │\n└─────────────────────────────┘{Colors.RESET}",
            "/home/eth/Documents/notas.txt": "Notas importantes:\n1. Recordar cambiar contraseña\n2. Revisar logs del sistema\n3. Actualizar software",
            "/etc/config.conf": "[sistema]\nversion=2.0\nhostname=EthOS\nsecurity_level=high",
        }
        
        print(contents.get(file_path, "[Archivo vacío]"))
    
    def cmd_mkdir(self, args):
        """Comando: mkdir [directorio] - Crear directorio"""
        if not args:
            print(f"{Colors.RED}[✗] Error: Debes especificar un nombre de directorio{Colors.RESET}")
            return
        
        dir_name = args[0]
        new_path = self.normalize_path(dir_name)
        
        if self.path_exists(new_path):
            print(f"{Colors.RED}[✗] Error: El directorio ya existe{Colors.RESET}")
            return
        
        # Agregar directorio simulado
        self.file_system[new_path] = {"type": "dir", "contents": []}
        parent_path = "/".join(new_path.rstrip("/").split("/")[:-1]) or "/"
        
        if parent_path in self.file_system:
            self.file_system[parent_path]["contents"].append(args[0])
        
        print(f"{Colors.GREEN}[��] Directorio creado: {new_path}{Colors.RESET}")
    
    def cmd_echo(self, args):
        """Comando: echo [texto] - Imprimir texto"""
        if not args:
            print()
            return
        
        text = " ".join(args)
        print(f"{Colors.YELLOW}{text}{Colors.RESET}")
    
    def cmd_easter(self, args):
        """Comando secreto: easter egg"""
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}")
        print("╔════════════════════════════════════════╗")
        print("║  🔓 MODO SECRETO DESBLOQUEADO 🔓      ║")
        print("╠════════════════════════════════════════╣")
        print("║  Bienvenido al nivel profundo...       ║")
        print("║  Acceso a archivos restringidos: OK    ║")
        print("║  Sistema de seguridad: DESACTIVADO     ║")
        print("║  Nivel administrativo: CONCEDIDO       ║")
        print("║                                        ║")
        print("║  Secreto encontrado: ✓                 ║")
        print("║  Puntos obtenidos: +100                ║")
        print("║                                        ║")
        print("║  ¡Eres un verdadero hacker! 🎉         ║")
        print("╚════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
    
    def cmd_exit(self, args):
        """Comando: exit - Salir del programa"""
        print(f"\n{Colors.RED}{Colors.BOLD}")
        print("╔═══════════════════════════════════════╗")
        print("║    SESIÓN FINALIZADA CORRECTAMENTE    ║")
        print("║    Datos guardados: [✓]               ║")
        print("║    Logs registrados: [✓]              ║")
        print("║    Hasta pronto, {:<20} ║".format(self.current_user))
        print("╚═══════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")
        sys.exit(0)
    
    def process_command(self, command_line):
        """Procesa el comando ingresado"""
        if not command_line.strip():
            return
        
        parts = command_line.strip().split()
        command = parts[0].lower()
        args = parts[1:]
        
        # Diccionario de comandos
        commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "pwd": self.cmd_pwd,
            "clear": self.cmd_clear,
            "help": self.cmd_help,
            "whoami": self.cmd_whoami,
            "date": self.cmd_date,
            "cat": self.cmd_cat,
            "mkdir": self.cmd_mkdir,
            "echo": self.cmd_echo,
            "easter": self.cmd_easter,
            "exit": self.cmd_exit,
        }
        
        if command in commands:
            self.history.append(command_line)
            try:
                commands[command](args)
            except Exception as e:
                print(f"{Colors.RED}[✗] Error: {str(e)}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[✗] Comando no reconocido: '{command}'{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Escribe 'help' para ver comandos disponibles{Colors.RESET}")
    
    def run(self):
        """Loop principal del simulador"""
        try:
            while True:
                try:
                    user_input = input(self.print_prompt())
                    self.process_command(user_input)
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}[!] Interrupción del usuario - Sesión cancelada{Colors.RESET}")
                    self.cmd_exit([])
                except EOFError:
                    self.cmd_exit([])
        except Exception as e:
            print(f"{Colors.RED}[✗] Error fatal: {str(e)}{Colors.RESET}")
            sys.exit(1)

def main():
    """Función principal"""
    try:
        simulator = UnixSimulator()
        simulator.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Sistema interrumpido{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()