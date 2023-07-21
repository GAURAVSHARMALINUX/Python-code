from Function import ssh_tunnel
import getpass
host=input(f"Enter the IP address: ").lower().replace(" ","") # Taking IP address from the user.
user=input(f"Enter user name: ").lower().strip().replace(" ","") # Asking for remote user name to make tunnel.
user_password = getpass.getpass('Password: ').strip().replace(" ","") # Asking for the password
#key=input(f"Enter the ssh-key file path: ").lower().strip()
port=int(input("Enter SSH port : ").lower().replace(" ",""))
ssh_tunnel(host,user,user_password,port)
