import paramiko
import sshtunnel
import getpass

host=input(f"Enter the IP address: ").lower().replace(" ","") # Taking IP address from the user.
user=input(f"Enter user name: ").lower().strip().replace(" ","") # Asking for remote user name to make tunnel.
user_password = getpass.getpass('Password: ').strip().replace(" ","") # Asking for the password
#key=input(f"Enter the ssh-key file path: ").lower().strip()
port=int(input("Enter SSH port : ").lower().replace(" ",""))
with sshtunnel.open_tunnel(
    (host, port),
    ssh_username=user,
    ssh_password=user_password,
    #ssh_pkey=key,
    #ssh_private_key_password="redhat",
    remote_bind_address=(host, port),
    local_bind_address=('0.0.0.0', 10022)
) as tunnel:
    while True:
        client = paramiko.SSHClient()
        disabled_algorithms={'keys': ['rsa-sha2-256', 'rsa-sha2-512']}
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host,username=user,password=user_password,look_for_keys=False)
