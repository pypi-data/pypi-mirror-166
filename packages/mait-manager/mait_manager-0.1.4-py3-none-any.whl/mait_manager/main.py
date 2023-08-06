# Import required modules
import typer # Turns mait_manager into a CLI tool.
import socket # Networking.
from alive_progress import alive_bar # Progress bar.
import os # Executing commands
import tempfile # Temporary folder.

app = typer.Typer(help="Package manager for text adventure games.", name="mait")

HOST = 'temperatecafe.com'
PORT = 8081

print(r"""
     /\__\         /\  \          ___        /\  \    
    /::|  |       /::\  \        /\  \       \:\  \   
   /:|:|  |      /:/\:\  \       \:\  \       \:\  \  
  /:/|:|__|__   /::\~\:\  \      /::\__\      /::\  \ 
 /:/ |::::\__\ /:/\:\ \:\__\  __/:/\/__/     /:/\:\__\
 \/__/~~/:/  / \/__\:\/:/  / /\/:/  /       /:/  \/__/
       /:/  /       \::/  /  \::/__/       /:/  /     
      /:/  /        /:/  /    \:\__\       \/__/      
     /:/  /        /:/  /      \/__/                  
     \/__/         \/__/                              
     """)

@app.command(help="Lists all packages in mait_manager's registry.")
def list():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connect to server.

        s.sendall(b"list") # Send 'list' command to server.
        recv_back = s.recv(1024).decode('UTF-8') # What the server returned.
        print(f"{recv_back}") # Prints the list of packages.
        s.close() # Close the connection.
        exit() # Exit the program.

@app.command(help="Creates a temporary file from requested package and executes it.")
def play(game):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connect to server.

        with alive_bar(3) as bar:
            concat = "1" + game
            command = bytes(concat.encode('UTF-8'))  # Sends 1package to server.
            s.send(command)
            command = s.recv(1024).decode('UTF-8')  # It will send back the command to run the script.
            bar()
            print(command)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            concat = "2" + game
            name = bytes(concat.encode('UTF-8'))  # Sends 2package to server.
            s.send(name)
            name = s.recv(1024).decode('UTF-8')  # Gets the name of the package
            bar()
            print(name)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            concat = "3" + game
            contents = bytes(concat.encode('UTF-8'))  # Sends 3package to server.
            s.send(contents)
            contents = s.recv(9999999).decode('UTF-8')  # Gets contents of the package
            bar()
            print(contents)
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            """
            We did 3 things:
            - Get the command to run the file,
            - Get the name of the file,
            - and get the contents.
            """

        with tempfile.TemporaryDirectory() as tmpdir:
            with open(f"{tmpdir}/{name}", 'x') as f:
                f.write(contents)

            os.chdir(tmpdir)
            os.system('clear')
            os.system(command)

@app.command(help="Uploads a package to mait_manager's registry for review.")
def upload():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connect to server.

        name = input("Enter new file name & extension: ")
        name = "4" + name
        s.send(bytes(name.encode('UTF-8')))
        response = s.recv(11).decode('UTF-8')
        if response == b"File exists!":
            print(response)
            exit()
        elif not response.isascii():
            pass

        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        file_dir = input("Enter directory of existing file: ")
        is_exist = os.path.exists(file_dir)
        if is_exist == False:
            print("Directory does not exist!")
            exit()

        with open(file_dir, 'r') as f:
            data = f.read()

        data = "5" + f"{name}|" + data
        s.send(bytes(data.encode('UTF-8')))
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        file_dir = input("Enter directory of existing json: ")
        is_exist = os.path.exists(file_dir)
        if is_exist == False:
            print("Directory does not exist!")
            exit()

        with open(file_dir, 'r') as f:
            data = f.read()

        index = name.find('.')
        name = name[:index].replace('4', '')
        data = "6" + f"{name}|" + data
        s.send(bytes(data.encode('UTF-8')))

if __name__ == "__main__":
    app()
