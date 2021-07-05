import os

# --- JupyterHub ---
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.cookie_secret = '288696652124211857713239dcd33bba50309572f4725ad4bc50107613fd7ba8'
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.log_level = 'DEBUG'
c.JupyterHub.admin_access = False

# --- ConfigurableHTTPProxy ---
c.ConfigurableHTTPProxy.pid_file = '/tmp/jupyterhub-proxy.pid'
c.ConfigurableHTTPProxy.auth_token = '39ddf85a0070c9ccab2db167e79af2bf03d795248939bf249cbb1d153f9a71c9'

# --- Database ---
c.JupyterHub.db_url = ':memory:'

# --- Users ---
c.Authenticator.allowed_users = {
    'jupyterhub',
    os.environ['USER'],
    }
c.Authenticator.admin_users = {
    'jupyterhub',
    os.environ['USER'],
    }

# --- Authenticator ---
from jupyterhub.auth import PAMAuthenticator
c.JupyterHub.authenticator_class = PAMAuthenticator
# c.PAMAuthenticator.open_sessions = False

# --- Spawner ---
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.Spawner.debug = True
c.Spawner.default_url = '/lab'
c.Spawner.cmd = ["jupyter-labhub"]
# Enable debug-logging of the single-user server
c.LocalProcessSpawner.debug = True
