#!/usr/bin/env python3 /usr/bin/python3
def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str
while True:
    print("#"*20,'\033[1m' +"Please choose an option from below"+"\033[0m","#"*20,"\n")
    main_menu=int(input("1. Generate keys\n2. Open an SSH tunnel\n3. Encrypt a file\n4. Decode the file.\n5. Exit\nChoose a number:=> ",))
    if main_menu in (1,2,3,4,5):
        if main_menu==1:
            to_user=input("To whome you want to share key, Please specified the name: ").lower().split()
            from subprocess import call
            import os
            key_store_path=os.environ['HOME'],"/.keys/",to_user[0]
            key_path=convertTuple(key_store_path)
            print("Key store dir path for given user: ", key_path)
            if os.path.isdir(key_path):
                print("User key already Generated at",key_path)
            else:
                print("Key file not there, Generating it")
                try:
                    os.makedirs(key_path, exist_ok = True)
                    print("Directory '%s' created successfully" % key_path)
                except OSError as error:
                    print("Directory '%s' can not be created" % key_path)
                private_key_file=key_path + "/" +to_user[0] + ".key"
                private_key_gen_command="/usr/bin/openssl genrsa -out " + private_key_file + " 4096"
                os.system(private_key_gen_command)

                public_key_file=key_path + "/" +to_user[0] + ".pub"
                public_key_gen_command="openssl rsa -in " + private_key_file + " -out " + public_key_file + " -pubout "
                os.system(public_key_gen_command)
                continue

        if main_menu==2:
            import paramiko
            import sshtunnel

            r_server_host=input(f"Please Enter the IP address of destination server: ").lower()
            r_server_user=input(f"Enter remote user name: ").lower().strip()
            #r_server_pass=input(f"Enter password : ").lower().strip()
            r_server_key=input(f"Enter the ssh-key file path: ").lower().strip()
            r_server_port=int(input("Enter SSH port : ").lower())
            with sshtunnel.open_tunnel(
                (r_server_host, r_server_port),
                ssh_username=r_server_user,
                #ssh_password=r_server_pass,
                ssh_pkey=r_server_key,
                #ssh_private_key_password="redhat",
                remote_bind_address=(r_server_host, r_server_port),
                local_bind_address=('0.0.0.0', 10022)
            ) as tunnel:
                while True:
                    client = paramiko.SSHClient()
                    disabled_algorithms={'keys': ['rsa-sha2-256', 'rsa-sha2-512']}
                    client.load_system_host_keys()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect('127.0.0.1', 10022, disabled_algorithms={'keys': ['rsa-sha2-256', 'rsa-sha2-512']})
                    # do some operations with client session
                    client.close()
                    continue

        if main_menu==3:
            file_to_user=input(f"To whom would you like to give the file: ").lower().split()
            from subprocess import call
            import os
            file_key_store_path=os.environ['HOME'],"/.keys/",file_to_user[0]
            file_key_path=convertTuple(file_key_store_path)
            print("Key store dir path for given user: ", file_key_path)
            file_public_key=file_key_path+"/"+file_to_user[0]+".pub"
            if os.path.isdir(file_key_path):
                file_to_encrypt=input("Which file you want to encrypt: ")
                encrypt_file_command="openssl pkeyutl -encrypt -pubin -inkey " + file_public_key + " -in " + file_to_encrypt + " -out " + file_to_encrypt + ".enc"
                os.system(encrypt_file_command)
            else:
                print("Private key not found for that user, Either generate the key pair for user or put the key file at location if already generated")
            continue



        if main_menu==4:
            dfile_to_user=input(f"From which user did you get this file? ").lower().split()
            from subprocess import call
            import os
            dfile_key_store_path=os.environ['HOME'],"/.keys/",dfile_to_user[0]
            dfile_key_path=convertTuple(dfile_key_store_path)
            print("Key store dir path for given user: ", dfile_key_path)
            dfile_private_key=dfile_key_path+"/"+dfile_to_user[0]+".key"
            print("Private Key file path: ", dfile_private_key)
            if os.path.isfile(dfile_private_key):
                dfile_to_decrypt=input("Which file you want to decrypt: ").strip()
                decrypt_file_command="openssl pkeyutl -decrypt -inkey " + dfile_private_key + " -in " + dfile_to_decrypt + " -out " + dfile_to_decrypt + "_decrypted"
                os.system(decrypt_file_command)
            else:
                print("Private key not found for that user, Either generate the key pair for user or put the key file at location if already generated")
            continue
        if main_menu==5:
            break


    else:
        print ('\033[1m'+"Please choose an valid option.\n\n"+'\033[0m')
        continue
