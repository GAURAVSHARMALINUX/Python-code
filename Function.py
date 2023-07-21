def ssh_tunnel (host,user,user_password,port):
    import paramiko
    import sshtunnel


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

