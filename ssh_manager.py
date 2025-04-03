import paramiko
import time
from concurrent.futures import ThreadPoolExecutor

class SSHManager:
    def __init__(self, radius_user, radius_pass, jump_host=None, jump_user=None, jump_pass=None):
        self.radius_user = radius_user
        self.radius_pass = radius_pass
        self.jump_host = jump_host
        self.jump_user = jump_user
        self.jump_pass = jump_pass
        self.timeout = 10  # Réduction du délai global
        self.command_timeout = 10  # Nouveau délai pour les commandes
        self.results = {}

    def _create_jump_channel(self, device):
        """Établit la connexion via le serveur de rebond"""
        try:
            jump_client = paramiko.SSHClient()
            jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            jump_client.connect(
                hostname=self.jump_host,
                username=self.jump_user,
                password=self.jump_pass,
                look_for_keys=False,
                allow_agent=False,
                timeout=self.timeout
            )
            channel = jump_client.get_transport().open_channel(
                'direct-tcpip', (device, 22), ('', 0)
            )
            channel.settimeout(self.timeout)  # Ajout d'un délai pour le canal
            return channel
        except paramiko.ChannelException as e:
            raise paramiko.SSHException(f"Échec connexion jump host: {str(e)}")
        except Exception as e:
            raise paramiko.SSHException(f"Erreur inattendue jump host: {str(e)}")

    def _execute_command(self, shell, command, password=None):
        shell.send(command + '\n')
        output = ""
        start_time = time.time()  # Suivi du temps écoulé
        waiting_for_password = False
        
        while True:
            time.sleep(0.5)
            if shell.recv_ready():
                chunk = shell.recv(4096).decode('utf-8')
                output += chunk
                
                # Détection de l'invite de mot de passe
                if 'Password:' in chunk and password:
                    shell.send(password + '\n')
                    waiting_for_password = False
                    continue
                    
                if '--More--' in chunk:
                    output = output.replace('--More--', '')
                    shell.send(' ')
                
                # Gestion de "Press any key to continue (Q to quit)"
                if 'Press any key to continue' in chunk:
                    shell.send(' ')
            else:
                if not output.strip():
                    continue
                if output.strip().endswith(command.strip()):
                    continue
                if ('#' in output[-20:] or '>' in output[-20:]) and not waiting_for_password:
                    break
            
            if time.time() - start_time > self.command_timeout:  # Arrêt si délai dépassé
                output += "\n[Timeout atteint pour la commande]"
                break
                
        return output.strip()

    def connect_and_execute(self, device, commands, admin_password=None):
        client = None
        result = {"status": "success", "output": []}
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.jump_host:
                try:
                    channel = self._create_jump_channel(device)
                except paramiko.SSHException as e:
                    result["status"] = "error"
                    result["output"].append(f"Erreur: {str(e)}")
                    return device, result

                client.connect(
                    hostname=device,
                    username=self.radius_user,
                    password=self.radius_pass,
                    sock=channel,
                    look_for_keys=False,
                    allow_agent=False,
                    timeout=self.timeout
                )
            else:
                client.connect(
                    hostname=device,
                    username=self.radius_user,
                    password=self.radius_pass,
                    look_for_keys=False,
                    allow_agent=False,
                    timeout=self.timeout
                )

            shell = client.invoke_shell()
            shell.settimeout(self.command_timeout)  # Utilisation du délai pour les commandes

            i = 0
            while i < len(commands):
                cmd = commands[i].strip()
                if cmd:
                    if cmd == 'enable-admin' and admin_password:
                        # Traitement spécial pour enable-admin avec mot de passe
                        output = self._execute_command(shell, cmd, admin_password)
                        result["output"].append(f"Commande: {cmd}\n{output}\n")
                    else:
                        output = self._execute_command(shell, cmd)
                        result["output"].append(f"Commande: {cmd}\n{output}\n")
                i += 1

        except Exception as e:
            result["status"] = "error"
            result["output"].append(f"Erreur: {str(e)}")
        finally:
            if client:
                client.close()
                
        return device, result

    def execute_on_devices(self, devices, commands, admin_password=None):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.connect_and_execute, device, commands, admin_password) for device in devices]
            for future in futures:
                device, result = future.result()
                self.results[device] = result
        return self.results
