# Password Manager CLI (Passwrd)

A simple command-line password manager built with Python that securely stores passwords using Fernet encryption. The encryption is based on a user-provided seed, ensuring that only users with the correct seed can access stored passwords.

## Features
- Secure password encryption using Fernet (AES-based encryption)
- Store multiple passwords for different websites and users
- Retrieve stored passwords and copy them to the clipboard
- Update existing passwords
- List stored websites and associated users
- Menu-driven interface for interactive use
- Command-line arguments for quick actions

## Installation

### 1. Install Dependencies
Ensure you have Python 3.12 installed, then install dependencies:
```sh
pip install -r dependencies.txt
```

### 2. Running the CLI
You can run the script interactively:
```sh
python3 main.py init --seed myseed
```
Or use command-line arguments for quick actions:
```sh
python main.py add --site example.com --user myemail@example.com --password mysecurepassword --seed myseed
```

## Usage

### Interactive Mode
Run the script and enter your encryption seed:
```sh
python main.py init --seed myseed
```
Follow the on-screen menu options to add, retrieve, update, or list passwords.

### Command-Line Mode

#### Add a Password
```sh
python main.py add --site example.com --user myemail@example.com --password mysecurepassword --seed myseed
```

#### Retrieve a Password
```sh
python main.py get --site example.com --user myemail@example.com --seed myseed
```

#### List Stored Websites
```sh
python main.py list --seed myseed
```

#### List Users for a Website
```sh
python main.py list-user --site example.com --seed myseed
```

#### Start Interactive Mode
```sh
python main.py init --seed myseed
```

## Creating an Executable
To bundle your script into a single executable file, follow these steps:

### 1. Install PyInstaller
```sh
pip install pyinstaller
```

### 2. Build the Executable
```sh
pyinstaller --onefile --name passwrd main.py
```

### 3. Run the Executable
After building, the executable will be in the `dist/` folder:
```sh
dist/passwrd
```

### 4. Add an Alias (Optional)
To run the password manager with a simple command, move the executable to `/usr/local/bin/` (Linux/macOS) or set it in `PATH` (Windows/Linux):
```sh
sudo mv dist/passwrd /usr/local/bin/
```
Now you can use:
```sh
passwrd init --seed myseed
```

## Dependencies
The project requires the following dependencies:
- `cryptography`
- `pyperclip`
- `colorama`

These are listed in `dependencies.txt`. Install them using:
```sh
pip install -r dependencies.txt
```

## Notes
- **The seed is required** to access stored passwords. If you forget your seed, **you cannot retrieve your passwords.**
- The passwords are stored in `passwords.json` in encrypted form.
- The password manager copies retrieved passwords to the clipboard for convenience.

## License
This project is open-source. Feel free to modify and use it as needed!

