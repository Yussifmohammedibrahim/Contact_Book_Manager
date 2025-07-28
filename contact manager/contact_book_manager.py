import json

def main():
    contacts = {}
    contact_ids = iter(range(101, 1000))  # More IDs for flexibility

    while True:
        print("\nContact Book Manager")
        print("1. Add New Contact")
        print("2. Edit Contact by ID")
        print("3. View All Contacts")
        print("4. Search Contacts by City")
        print("5. Show Summary")
        print("6. Delete Contact by ID")
        print("7. Save/Load Contacts")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_contact_menu(contacts, contact_ids)
        elif choice == "2":
            edit_contact_menu(contacts)
        elif choice == "3":
            view_contacts(contacts)
        elif choice == "4":
            search_by_city_menu(contacts)
        elif choice == "5":
            show_summary(contacts)
        elif choice == "6":
            delete_contact_menu(contacts)
        elif choice == "7":
            save_load_menu(contacts)
        elif choice == "8":
            save_contacts_to_file(contacts)  # Auto-save on exit
            print("\nGoodbye! Your contacts have been saved.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

# --- Contact CRUD Functions ---

def add_contact_menu(contacts, contact_ids):
    print("\nAdd New Contact")

    name = input("Enter contact name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter contact name: ").strip()

    phone = input("Enter phone number (10 digits): ").strip()
    while not phone.isdigit() or len(phone) != 10:
        print("Phone number must be exactly 10 digits.")
        phone = input("Enter phone number (10 digits): ").strip()

    city = input("Enter city: ").strip().title()
    while not city:
        print("City cannot be empty.")
        city = input("Enter city: ").strip().title()

    contact_id = next(contact_ids, None)
    if contact_id is not None:
        contacts[contact_id] = {"name": name, "phone": phone, "city": city}
        print(f"Contact added successfully! Assigned ID: {contact_id}")
    else:
        print("No more contact IDs available.")

def edit_contact_menu(contacts):
    if not contacts:
        print("\nNo contacts available to edit.")
        return

    try:
        contact_id = int(input("\nEnter contact ID to edit: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    if contact_id not in contacts:
        print(f"No contact found with ID: {contact_id}")
        return

    contact = contacts[contact_id]
    print(f"\nEditing Contact (ID: {contact_id})")
    print(f"Current Name: {contact['name']}")
    print(f"Current Phone: {contact['phone']}")
    print(f"Current City: {contact['city']}")

    new_name = input("Enter new name (leave blank to keep current): ").strip()
    if new_name:
        contact['name'] = new_name

    new_phone = input("Enter new phone (10 digits, leave blank to keep current): ").strip()
    if new_phone:
        while not new_phone.isdigit() or len(new_phone) != 10:
            print("Phone number must be exactly 10 digits.")
            new_phone = input("Enter new phone (10 digits): ").strip()
        contact['phone'] = new_phone

    new_city = input("Enter new city (leave blank to keep current): ").strip().title()
    if new_city:
        contact['city'] = new_city

    print(f"Contact (ID: {contact_id}) updated successfully.")

def delete_contact_menu(contacts):
    if not contacts:
        print("\nNo contacts available to delete.")
        return

    try:
        contact_id = int(input("\nEnter contact ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    if contact_id in contacts:
        confirm = input(f"Are you sure you want to delete contact ID {contact_id}? (y/n): ").lower()
        if confirm == 'y':
            del contacts[contact_id]
            print("Contact deleted successfully.")
        else:
            print("Deletion canceled.")
    else:
        print(f"No contact found with ID: {contact_id}")

# --- Viewing and Searching ---

def view_contacts(contacts):
    if not contacts:
        print("\nNo contacts available.")
        return

    print("\nAll Contacts (Sorted by Name):")
    sorted_contacts = sorted(contacts.items(), key=lambda item: item[1]["name"].lower())

    for cid, info in sorted_contacts:
        print(f"- ID: {cid}, Name: {info['name']}, Phone: {info['phone']}, City: {info['city']}")

def search_by_city_menu(contacts):
    if not contacts:
        print("\nNo contacts available to search.")
        return

    city = input("\nEnter city to search for: ").strip().title()
    results = {cid: info for cid, info in contacts.items() if info["city"] == city}

    if results:
        print(f"\nContacts in {city}:")
        for cid, info in results.items():
            print(f"- ID: {cid}, Name: {info['name']}, Phone: {info['phone']}")
    else:
        print(f"No contacts found in {city}")

def show_summary(contacts):
    if not contacts:
        print("\nNo contacts available for summary.")
        return

    cities = {info["city"] for info in contacts.values()}
    longest_name = max((info["name"] for info in contacts.values()), key=len, default="")

    print("\nContact Book Summary:")
    print(f"- Total contacts: {len(contacts)}")
    print(f"- Unique cities: {len(cities)}")
    print(f"- Cities: {', '.join(sorted(cities))}")
    print(f"- Contact with longest name: {longest_name} ({len(longest_name)} characters)")

# --- Save and Load ---

def save_contacts_to_file(contacts, filename="contacts.json"):
    try:
        with open(filename, "w") as f:
            json.dump(contacts, f)
        print("Contacts saved successfully.")
    except Exception as e:
        print(f"Error saving contacts: {e}")
        

def load_contacts_from_file(filename="contact.json"):
    try:
        with open(filename, "r") as f:
            contacts = json.load(f)
        # Convert keys back to int
        return {int(k): v for k, v in contacts.items()}
    except FileNotFoundError:
        print("No saved contacts found.")
        return {}
    except Exception as e:
        print(f"Error loading contacts: {e}")
        return {}

def save_load_menu(contacts):
    print("\nSave/Load Menu:")
    print("1. Save to File")
    print("2. Load from File")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        save_contacts_to_file(contacts)
    elif choice == "2":
        loaded = load_contacts_from_file()
        if loaded:
            contacts.clear()
            contacts.update(loaded)
            print("Contacts loaded successfully.")
    else:
        print("Invalid choice.")
if __name__ == "__main__":
    main()