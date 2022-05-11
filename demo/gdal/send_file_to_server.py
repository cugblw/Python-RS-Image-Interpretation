import os
import paramiko

# center = [103.73352,36.08428]
# zoom = 15
# http://10.141.3.40:10001/service/map/satellite-test?z={z}&x={x}&y={y}
# http://10.141.3.40:10001/service/map/satellite-test?z=16&x=51632&y=25706

def send_file_to_server(ftp_client, file_name, local_path, server_path):
    local_tar_path = os.path.join(local_path, file_name).replace('\\','/')
    server_tar_path = os.path.join(server_path, file_name).replace('\\','/')
    ftp_client.put(local_tar_path, server_tar_path)
    return None

def unzip_server_file(ssh_client, server_tar_path, sever_tile_path):
    return None

def write_log_file(file_path, file_list):
    # log_file = open('C:/Users/Administrator/Desktop/tar_list.txt', 'w')
    log_file = open(os.path.join(file_path,'tar_list.txt').replace('\\','/'), 'w')
    log_file.writelines([line+'\n' for line in file_list])
    log_file.close()

def send_log_file(ftp_client, file_path, server_path):
    log_file = os.path.join(file_path, 'tar_list.txt').replace('\\','/')
    server_log_path = os.path.join(server_path, 'tar_list.txt').replace('\\','/')
    ftp_client.put(log_file, server_log_path)


if __name__ == '__main__':
    result_path = 'C:/Users/Administrator/Desktop/tar_list'
    sever_tar_path = '/data1/satetar_data/20220509'
    sever_tile_path = '/data1/nginx_data/satellite-test'

    # login
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh_client.connect(hostname='10.141.3.40', port=22, username='root', password='Navinfocloud')
    ssh_client.connect(hostname='10.141.3.40', username='root', password='Navinfocloud')
    ftp_client = ssh_client.open_sftp()

    tar_file_list = []
    for root, dirs, files in os.walk(result_path):
        for file in files:
            if file.endswith(".tar"):
                print(os.path.join(root, file))
                tar_file_list.append(file)
                # tar_file_path = os.path.join(root, file)
                send_file_to_server(ftp_client, file, result_path, sever_tar_path)

    write_log_file(result_path, tar_file_list)
    send_log_file(ftp_client, result_path, sever_tar_path)
    ftp_client.close()

    # unzip
    unzip_command = 'cd ' + sever_tar_path+ '; for tar in *.tar;  do tar -mxvf$tar -C ' + sever_tile_path + '; done'
    stdin, stdout, stderr = ssh_client.exec_command(unzip_command)
    print(stdout.read().decode())

    # access files
    access_command = 'cd ' + sever_tile_path + '; ls'
    stdin, stdout, stderr = ssh_client.exec_command(access_command)
    print(stdout.read().decode())

    # move tile folders
    move_command = 'cd ' + sever_tile_path + '/satellite;' + ' mv * ' + sever_tile_path
    stdin, stdout, stderr = ssh_client.exec_command(move_command)

    # delete empty folders
    delete_command = 'cd ' + sever_tile_path + ';' + ' rm -rf satellite'
    stdin, stdout, stderr = ssh_client.exec_command(delete_command)
    print(stdout.read().decode())

    # close connection
    ssh_client.close()