import secrets
import string
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Create a Rich console object
console = Console()

# Function to generate a strong password
def generate_pd(l=16):  # Define length of password
    chara = string.ascii_letters + string.digits + "!@#$%^&*()"
    pd = ''.join(secrets.choice(chara) for _ in range(l))
    return pd

# Function to save or update details in the text file
def save_to_file(platform, username, password, update=False):
    filename = "password_list.txt"
    entry = f"platform: {platform}\nUsername: {username}\nPassword: {password}\n\n"
    
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        updated_lines = []
        found = False

        # Iterate through the lines and try to find matching platform and username
        for i in range(0, len(lines), 4):
            if (
                lines[i].strip() == f"platform: {platform}"
                and lines[i + 1].strip() == f"Username: {username}"
            ):
                if update:
                    updated_lines.append(entry)  # Update the entry with new password
                else:
                    updated_lines.extend(lines[i:i+4])  # Keep the original entry if no update
                found = True
            else:
                updated_lines.extend(lines[i:i+4])  # Keep other entries intact

        # If no matching entry was found, append a new one
        if not found:
            updated_lines.append(entry)

        with open(filename, "w") as file:
            file.writelines(updated_lines)

        if found and update:
            console.print(f"[green]Password updated successfully for {platform} and {username}.[/green]")
        elif not found:
            console.print(f"[green]New entry added for {platform} and {username}.[/green]")

    except FileNotFoundError:
        # If the file doesn't exist, create a new one and add the entry
        with open(filename, "w") as file:
            file.write(entry)
        console.print(f"[green]Details saved to {filename}.[/green]")

# Function to search for a platform in the file
def search_platform(platform_name):
    filename = "password_list.txt"
    try:
        with open(filename, "r") as file:
            data = file.read()
            # Split entries by double newlines
            entries = data.strip().split("\n\n")
            for entry in entries:
                if f"platform: {platform_name}" in entry:
                    console.print(Panel(entry, title=f"[cyan]Details for {platform_name}[/cyan]", style="green"))
                    return
            console.print(Panel(f"No details found for the platform: [red]{platform_name}[/red]", style="red"))
    except FileNotFoundError:
        console.print(Panel("[bold red]No saved file found![/bold red] Create some entries first.", style="red"))

# Function to handle updating an existing password
def update_password():
    console.print(Panel.fit("[bold blue]Update Password[/bold blue]", style="cyan"))
    platform = console.input("[yellow]Enter the platform name:[/yellow] ")
    username = console.input("[yellow]Enter the username:[/yellow] ")

    filename = "password_list.txt"
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        for i in range(0, len(lines), 4):
            if (
                lines[i].strip() == f"platform: {platform}"
                and lines[i + 1].strip() == f"Username: {username}"
            ):
                new_password = generate_pd()
                save_to_file(platform, username, new_password, update=True)
                return

        console.print(f"[red]No matching entry found for platform {platform} and username {username}.[/red]")
    except FileNotFoundError:
        console.print("[bold red]No saved file found! Create some entries first.[/bold red]")

# Function to handle adding a new entry
def add_new_entry():
    console.print(Panel.fit("[bold blue]New Entry[/bold blue]", style="cyan"))
    platform = console.input("[yellow]Enter the platform name:[/yellow] ")
    username = console.input("[yellow]Enter the username/phone no./email:[/yellow] ")

    # Generate a unique password
    password = generate_pd()

    # Display details in a formatted table
    table = Table(title="Generated Password Details", style="magenta")
    table.add_column("Field", style="bold green")
    table.add_column("Value", style="bold yellow")
    table.add_row("platform", platform)
    table.add_row("Username", username)
    table.add_row("Password", password)

    console.print(table)

    # Save the details to a text file
    save_to_file(platform, username, password)

# Main menu function
def main_menu():
    while True:
        console.print(Panel.fit("[bold blue]Password Manager[/bold blue]", style="cyan"))
        console.print("[1] Add New Entry")
        console.print("[2] Check Stored Data")
        console.print("[3] Update Existing Password")
        console.print("[0] Exit")

        choice = console.input("[bold yellow]Enter your choice: [/bold yellow] ")

        if choice == "1":
            add_new_entry()
        elif choice == "2":
            platform_name = console.input("[yellow]Enter the platform name to search:[/yellow] ")
            search_platform(platform_name)
        elif choice == "3":
            update_password()
        elif choice == "0":
            console.print("[bold green]Exiting Password Manager. Goodbye![/bold green]")
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main_menu()
