import paramiko
from scp import SCPClient

__author__ = 'patryk.damec@gmail.com'


class SshService:
    """
    Estabilishing connection through SSH.
    Possible file transfer through SCP.
    """
    def __init__(self, host, username, password, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def setup_ssh(self):
        """
        Estabilishing SSH connection.
        :return: connection object
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username=self.username, hostname=self.host,
                    password=self.password, port=self.port)
        return ssh

    def execute_remote_command(self, command):
        """
        Executing command on remote server
        :param command: command to be executed remotely.
               Derrived from settings.py module
        :return: STDOUT of the command.
        """
        ssh = self.setup_ssh()
        stdin, stdout, stderr = ssh.exec_command(command)
        output_lines = stdout.read().strip()
        ssh.close()
        return output_lines

    def set_scp(self, localpath, remotepath):
        """
        Set SCP client to transport file.
        :param localpath: path file on local host.
        :param remotepath: path on remote server
        """
        ssh = self.setup_ssh()
        scpclient = SCPClient(ssh.get_transport(), socket_timeout=15.0)
        scpclient.put(localpath, remotepath)
        ssh.close()
