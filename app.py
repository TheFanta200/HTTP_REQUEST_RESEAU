# app.py
from flask import Flask, render_template, request
from ssh_manager import SSHManager

app = Flask(__name__)
app.secret_key = 'vtretertret'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupération des informations de connexion
        jump_host = request.form['jump_host'].strip()
        jump_user = request.form['jump_user'].strip()
        jump_pass = request.form['jump_pass'].strip()
        radius_user = request.form['radius_user'].strip()
        radius_pass = request.form['radius_pass'].strip()
        devices = [d.strip() for d in request.form['devices'].split('\n') if d.strip()]
        commands = [c.strip() for c in request.form['commands'].split('\n') if c.strip()]

        # Variable pour stocker le mot de passe admin si nécessaire
        admin_password = None
        
        # Vérification si le bouton "nokia_enable_admin" a été cliqué
        if 'nokia_enable_admin' in request.form:
            admin_password = request.form['enable_admin_password'].strip()
            commands.insert(0, 'enable-admin')  # Ajout uniquement de la commande enable-admin
        
        # Création du gestionnaire SSH
        ssh_manager = SSHManager(
            radius_user=radius_user,
            radius_pass=radius_pass,
            jump_host=jump_host,
            jump_user=jump_user,
            jump_pass=jump_pass
        )

        # Exécution des commandes
        results = ssh_manager.execute_on_devices(devices, commands, admin_password)
        return render_template('results.html', results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
