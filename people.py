#This file is for creating all the functionality of managing people in a mysql database
#Some of the fields will include First Name, Last Name, Address, Phone Number, Email, and Notes, Job Title, and Company, availitiy, and skills, education, favorite color, and birthday, favorite foods and other important information related to a persons identity
#This file will also include the ability to add, delete, and update people in the database
#This file will also include the ability to search for people in the database
#This file will also include the ability to list all the people in the database
#This file will also keep track of statistics related to people in the database such as the number of people in the database and the number of people with a certain job title
#This file will also include the ability to sort people by a certain field such as first name, last name, job title, company, and birthday
#This file will also include the ability to export the people in the database to a csv file
#This file will also include the ability to import people from a csv file into the database
#This file will also include the ability to print out a report of the people in the database
#This file will also include the ability to print out a report of the people in the database sorted by a certain field such as first name, last name, job title, company, and birthday
import sqlite3
import csv
import re
from datetime import datetime

class Person:
    def __init__(self, id, first_name, last_name, address, phone_number, email, notes, job_title, company, skills, education, favorite_color, birthday, favorite_foods):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.notes = notes
        self.job_title = job_title
        self.company = company
        self.skills = skills
        self.education = education
        self.favorite_color = favorite_color
        self.birthday = birthday
        self.favorite_foods = favorite_foods

class PeopleManager:
    def __init__(self):
        self.db_connection = sqlite3.connect('people_db.sqlite3')
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                address TEXT,
                phone_number TEXT,
                email TEXT,
                notes TEXT,
                job_title TEXT,
                company TEXT,
                skills TEXT,
                education TEXT,
                favorite_color TEXT,
                birthday TEXT,
                favorite_foods TEXT
            )
        """)
        self.db_connection.commit()
        cursor.close()

    def create_database_if_not_exists(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS people_db")

    def add_person(self, person):
        # Validate the person before adding
        self.validate_person(person)

        cursor = self.db_connection.cursor()
        person_data = {
            'first_name': person.first_name.strip(),
            'last_name': person.last_name.strip(),
            'address': person.address or "N/A",
            'phone_number': person.phone_number or "N/A",
            'email': person.email or "N/A",
            'notes': person.notes or "N/A",
            'job_title': person.job_title or "N/A",
            'company': person.company or "N/A",
            'skills': str(person.skills) or "N/A",
            'education': str(person.education) or "N/A",
            'favorite_color': str(person.favorite_color) or "N/A",
            'birthday': person.birthday or "N/A",
            'favorite_foods': str(person.favorite_foods) or "N/A"
        }
        placeholders = ', '.join(['?'] * len(person_data))
        sql = f"INSERT INTO people ({', '.join(person_data.keys())}) VALUES ({placeholders})"
        cursor.execute(sql, list(person_data.values()))
        self.db_connection.commit()
        cursor.close()

    def validate_person(self, person):
        if not person.first_name or not person.last_name:
            raise ValueError("First name and last name are required.")

    def search_person_by_first_name(self, first_name):
        cursor = self.db_connection.cursor()
        sql = "SELECT * FROM people WHERE LOWER(first_name) = LOWER(?)"
        cursor.execute(sql, (first_name,))
        results = cursor.fetchall()
        cursor.close()
        return results if results else []

    def delete_person(self, person_id):
        cursor = self.db_connection.cursor()
        sql = "DELETE FROM people WHERE id = ?"
        cursor.execute(sql, (person_id,))
        self.db_connection.commit()
        cursor.close()

    def edit_person_field(self, person_id, field, new_value):
        cursor = self.db_connection.cursor()
        sql = f"UPDATE people SET {field} = ? WHERE id = ?"
        cursor.execute(sql, (new_value, person_id))
        self.db_connection.commit()
        cursor.close()

    def search_people(self, search_term):
        cursor = self.db_connection.cursor()
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'notes', 'job_title', 'company', 'skills', 'education', 'favorite_color', 'birthday', 'favorite_foods']
        sql = "SELECT * FROM people WHERE " + " OR ".join(f"{field} LIKE ?" for field in fields)
        cursor.execute(sql, ['%' + search_term + '%'] * len(fields))
        results = cursor.fetchall()
        return [tuple(result) for result in results]

    def list_all_people(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM people")
        return cursor.fetchall()

    def sort_people(self, sort_field):
        cursor = self.db_connection.cursor()
        cursor.execute(f"SELECT * FROM people ORDER BY {sort_field}")
        return cursor.fetchall()

    def update_person(self, person_name, updated_data):
        cursor = self.db_connection.cursor()
        sql = "UPDATE people SET " + ", ".join(f"{key} = %s" for key in updated_data.keys()) + " WHERE id = %s"
        cursor.execute(sql, list(updated_data.values()) + [person_name])
        self.db_connection.commit()

    def search_people(self, search_term):
        cursor = self.db_connection.cursor()
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'notes', 'job_title', 'company', 'skills', 'education', 'favorite_color', 'birthday', 'favorite_foods']
        sql = "SELECT * FROM people WHERE " + " OR ".join(f"{field} LIKE ?" for field in fields)
        cursor.execute(sql, ['%' + search_term + '%'] * len(fields))
        results = cursor.fetchall()
        return [tuple(result) for result in results]

    def list_all_people(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM people")
        return cursor.fetchall()

    def sort_people(self, sort_field):
        cursor = self.db_connection.cursor()
        cursor.execute(f"SELECT * FROM people ORDER BY {sort_field}")
        return cursor.fetchall()

    def export_people_to_csv(self, csv_file_path):
        people = self.list_all_people()
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(people)

    def import_people_from_csv(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                person = Person(*row)
                self.add_person(person)

    def print_people_report(self):
        people = self.list_all_people()
        for person in people:
            print(', '.join(str(x) for x in person))

    def print_sorted_people_report(self, sort_field):
        people = self.sort_people(sort_field)
        for person in people:
            print(', '.join(str(x) for x in person))