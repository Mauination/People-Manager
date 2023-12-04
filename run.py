from people import PeopleManager, Person
import people
import re
from datetime import datetime
from prettytable import PrettyTable

def add_person(manager):
    first_name = input("Enter first name: ")
    while not first_name:
        print("First name is required.")
        first_name = input("Enter first name: ")

    last_name = input("Enter last name: ")
    while not last_name:
        print("Last name is required.")
        last_name = input("Enter last name: ")

    address = input("Enter address: ") or "N/A"

    phone_number = input("Enter phone number: ") or "N/A"

    email = input("Enter email: ") or "N/A"

    notes = input("Enter notes: ") or "N/A"
    job_title = input("Enter job title: ") or "N/A"
    company = input("Enter company: ") or "N/A"
    skills = input("Enter skills (comma-separated): ").split(',') if input else ["N/A"]
    education = input("Enter education (comma-separated): ").split(',') if input else ["N/A"]
    favorite_color = input("Enter favorite color: ") or "N/A"

    birthday = input("Enter birthday (YYYY-MM-DD): ")
    while birthday:
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid birthday. Please try again in the format YYYY-MM-DD.")
            birthday = input("Enter birthday (YYYY-MM-DD): ")
    if not birthday:
        birthday = "N/A"

    favorite_foods = input("Enter favorite foods (comma-separated): ").split(',') if input else ["N/A"]

    # Create a Person instance and add it to the database
    person = Person(id, first_name, last_name, address, phone_number, email, notes, job_title, company, skills, education, favorite_color, birthday, favorite_foods)
    manager.add_person(person)

def edit_person(manager):
    person_name = input("Enter the name of the person to edit: ")
    people = manager.search_person_by_first_name(person_name)

    if not people:
        print("No person found.")
        return

    person = people[0]

    fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'notes', 'job_title', 'company', 'skills', 'education', 'favorite_color', 'birthday', 'favorite_foods']  # Add all valid column names here

    print("Which field would you like to update?")
    for i, field in enumerate(fields, start=1):
        print(f"{i}. {field}")

    field_number = int(input("Enter the number of the field: "))
    if 1 <= field_number <= len(fields):
        field = fields[field_number - 1]
    else:
        print("Invalid selection")
        return

    new_value = input(f"Enter the new value for {field}: ")
    manager.edit_person_field(person[0], field, new_value)  # Assuming person[0] is the id
def delete_person(manager):
    # Get person name from user input
    person_name = input("Enter the name of the person to delete: ")

    # Search for the person in the database
    people = manager.search_person_by_first_name(person_name)

    if not people:
        print("No person found.")
        return

    person = people[0]

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {person[0]} {person[1]}? (yes/no): ")  # Changed this line
    if confirm.lower() in ['yes','y']:
        # Delete the person from the database
        manager.delete_person(person[0])  # Changed this line
        print("Person deleted successfully.")

def view_all_people(manager, page=1):
    # Get all people from the database
    people = manager.list_all_people()

    # Calculate the range of people to display
    start = (page - 1) * 10
    end = start + 10

    # Create a table
    table = PrettyTable(['First Name', 'Last Name', 'Phone Number', 'Notes'])

    # Add people to the table
    for person_data in people[start:end]:
        person = Person(*person_data)
        table.add_row([person.first_name, person.last_name, person.phone_number, person.notes])

    # Print the table
    print(table)

    # Print the navigation options
    print("Page:", page)
    print("1. Next page")
    print("2. Previous page")
    print("3. Back to menu")

    # Get the user's choice
    choice = input("Enter your choice: ")

    # Navigate to the next or previous page or back to the menu
    if choice == '1' and end < len(people):
        view_all_people(manager, page + 1)
    elif choice == '2' and start > 0:
        view_all_people(manager, page - 1)

def search_person(manager):
    # Get search term from user input
    search_term = input("Enter a name to search for: ")

    # Search for the person in the database
    people = manager.search_people(search_term)

    # Display each person's details on a separate page
    for person_data in people:
        person = Person(*person_data)  # Exclude the first field (ID)

        # Print the person's details
        print(f"First Name: {person.first_name}")
        print(f"Last Name: {person.last_name}")
        print(f"Notes: {person.notes}")
        print(f"Phone Number: {person.phone_number}")
        print(f"Favorite Color: {person.favorite_color}")

        # Ask the user if they want to interact with this person
        interact = input("Do you want to interact with this person? (yes/no): ")
        if interact.lower() in ['yes','y']:
            while True:
                # Display a menu of options
                print("1. Update person")
                print("2. Delete person")
                print("3. Go back")
                option = input("Choose an option: ")
                if option == '1':
                    # Update person
                    fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'notes', 'job_title', 'company', 'skills', 'education', 'favorite_color', 'birthday', 'favorite_foods']  # Add all valid column names here

                    print("Which field would you like to update?")
                    for i, field in enumerate(fields, start=1):
                        print(f"{i}. {field}")

                    field_number = int(input("Enter the number of the field: "))
                    if 1 <= field_number <= len(fields):
                        field_to_update = fields[field_number - 1]
                    else:
                        print("Invalid selection")
                        return

                    new_value = input(f"Enter the new value for {field_to_update}: ")
                    manager.edit_person_field(person.id, field_to_update, new_value)  # Changed this line
                    print("Person updated successfully.")
                elif option == '2':
                    # Delete person
                    confirm = input("Are you sure you want to delete this person? (yes/no): ")
                    if confirm.lower() in ['yes','y']:
                        manager.delete_person(person.first_name)
                        print("Person deleted successfully.")
                        break
                elif option == '3':
                    break
                else:
                    print("Invalid option. Please try again.")

        input("Press enter to continue to the next person...")

def main():
    # Create a PeopleManager instance
    manager = people.PeopleManager()
    while True:
        # Print ASCII art and menu
        print("""
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |  <USER>               | |
              | |  |     Personnel      | |
              | |  |_       Manager     | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
                \_____     []     _______/
                    /______________\       

        1. Add a person
        2. Edit a person
        3. Delete a person
        4. View all people
        5. Search for a person
        6. Exit
        """)

        # Get user's choice
        choice = input("Enter your choice: ")

        # Perform the chosen operation
        if choice == '1':
            add_person(manager)
        elif choice == '2':
            edit_person(manager)
        elif choice == '3':
            delete_person(manager)
        elif choice == '4':
            view_all_people(manager)
        elif choice == '5':
            search_person(manager)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()