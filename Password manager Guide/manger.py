import secrets
import string

# Function to generate a strong password

def generate_pd(l=16):  #define length of password
    chara = string.ascii_letters + string.digits + "!@#$%^&*()"
    pd = ''.join(secrets.choice(chara) for _ in range(l))
    return pd

# Function to save the details into a text file

def save_to_file(service, username, password):
    filename = "password_lsit.txt"
    with open(filename, "a") as file:
        file.write(f"Service: {service}\nUsername: {username}\nPassword: {password}\n\n")
    print(f"Details saved to {filename}.")

# Main function to interact with the user and ask for certain details realted to account

def main():
    print("\nPassword Manager")
    service = input("Enter the service name: ")
    username = input("Enter the username: ")

    # Generate a unique password
    password = generate_pd()

    # Save the details to a text file
    save_to_file(service, username, password)

if __name__ == "__main__":
    main()
