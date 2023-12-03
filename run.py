# i want this to import and use the people.py functions 
# i want this to be strictly for displaying the data and interacting with the database but mostly focused on displaying the data and functionality with the people.py functionsfrom people import PeopleManager
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
    person = Person(first_name, last_name, address, phone_number, email, notes, job_title, company, skills, education, favorite_color, birthday, favorite_foods)
    manager.add_person(person)

def edit_person(manager):
    # Get person first name from user input
    person_first_name = input("Enter the first name of the person to edit: ")

    # Search for the person in the database
    people = manager.search_person_by_first_name(person_first_name)

    if len(people) > 1:
        # If multiple people are found, confirm the last name
        person_last_name = input("Multiple people found. Enter the last name: ")
        people = [person for person in people if person.last_name == person_last_name]

    if len(people) == 1:
        # If only one person is found, confirm if that's the person to update
        person = people[0]
        print(f"Person found: {person.first_name} {person.last_name}")
        confirm = input("Is this the person you want to update? (yes/no): ")
        if confirm.lower() == 'yes':
            # Ask which field to update
            field = input("Which field would you like to update? ")
            new_value = input(f"Enter new value for {field}: ")
            manager.edit_person_field(person.id, field, new_value)
        else:
            print("Operation cancelled.")
    else:
        print("No person found.")

def delete_person(manager):
    # Get person name from user input
    person_name = input("Enter the name of the person to delete: ")

    # Delete the person from the database
    manager.delete_person(person_name)

def view_all_people(manager, page=1):
    # Get all people from the database
    people = manager.list_all_people()

    # Calculate the range of people to display
    start = (page - 1) * 10
    end = start + 10

    # Create a table
    table = PrettyTable(['First Name', 'Last Name', 'Notes', 'Phone Number', 'favorite_color'])

    # Add people to the table
    for person_data in people[start:end]:
        person = Person(*person_data)
        table.add_row([person.first_name, person.last_name, person.notes, person.phone_number, person.favorite_color])

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
        if interact.lower() == 'yes':
            while True:
                # Display a menu of options
                print("1. Update person")
                print("2. Delete person")
                print("3. Go back")
                option = input("Choose an option: ")

                if option == '1':
                    # Update person
                    field_to_update = input("Enter the field you want to update: ")
                    new_value = input("Enter the new value: ")
                    manager.update_person(person.first_name, {field_to_update: new_value})
                    print("Person updated successfully.")
                elif option == '2':
                    # Delete person
                    confirm = input("Are you sure you want to delete this person? (yes/no): ")
                    if confirm.lower() == 'yes':
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
        _______________________
        |  _________________  |
        | | Pythonista      | |
        | |_________________| |________________
        |  ___ ___ ___   ___   ______________  |
        | | 7 | 8 | 9 | | + | |              | |
        | |___|___|___| |___| |              | |
        | | 4 | 5 | 6 | | - | |              | |
        | |___|___|___| |___| |              | |
        | | 1 | 2 | 3 | | x | |              | |
        | |___|___|___| |___| |______________| |
        | | . | 0 | = | | / |  _____________  |
        | |___|___|___| |___| |_____________| |
        |_____________________|

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