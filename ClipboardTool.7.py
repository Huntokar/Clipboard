import PySimpleGUI as sg
from tinydb import TinyDB, Query
import pyperclip
import subprocess
import os
import sys


def Delete_Scripts():
    # Initialize the TinyDB database
    db = TinyDB('data.json')
    # Define a Query object
    query = Query()

    # Get the list of documents from the TinyDB database
    documents = db.all()

    # Define the layout for the window
    layout = [
    [sg.Listbox(values=[doc['name'] for doc in documents], size=(30, 6), key='-DOCS-')],
    [sg.Button('Delete Selected Document'), sg.Text('', size=(30, 1), key='-OUTPUT-')],
    [sg.Button('Exit')]
    ]

    # Create the window
    window = sg.Window('TinyDB Document Selector and Deletion', layout)

    # Event loop to process events and get values from elements
    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Handle the button click event for deleting the selected document
        if event == 'Delete Selected Document':
            # Get the selected document from the listbox
            selected_document_name = values['-DOCS-'][0]

            # Remove the selected document from the TinyDB database
            db.remove(query.name == selected_document_name)

            # Update the output text element with a message
            window['-OUTPUT-'].update(f'Document "{selected_document_name}" deleted successfully.')

    # Close the TinyDB database and the window
    db.close()
    window.close()

def Add_Scripts():
    db = TinyDB('data.json')

    # Define the layout for the window
    layout = [
        [sg.Text("Enter your Script Name:"), sg.InputText(key='-NAME-', size=(30, 1))],
        [sg.Text("Enter your Script:"), sg.Multiline(key='-DATA-', size=(30, 10))],
        [sg.Button("Submit"), sg.Button("Exit")],
        [sg.Text("", size=(30, 1), key='-OUTPUT-')]
    ]

    # Create the window
    window = sg.Window("Data Entry", layout)

    # Event loop to process events and get values from elements
    while True:
        event, values = window.read()

        # Exit the program if the window is closed
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Handle the button click event
        if event == 'Submit':
            # Get the input values from the input fields
            name = values['-NAME-']
            data = values['-DATA-']

            # Update the output text element with the input values
            window['-OUTPUT-'].update(f"Name: {name}, Data: {data}")

            # Insert the input data into the TinyDB database as a dictionary
            db.insert({'name': name, 'data': data})

            # Clear the input fields after each entry
            window['-NAME-'].update('')
            window['-DATA-'].update('')

    # Close the TinyDB database and the window
    db.close()
    window.close()








# Initialize the TinyDB database
db = TinyDB('data.json')

sg.theme('dark green 1')

# Get the documents from the TinyDB database
documents = db.all()

# Create button layout with 3 buttons per row
buttons_layout = [
    [sg.Button(doc.get('name', 'N/A'), key=f'-DOC-{doc.doc_id}-') for doc in documents[i:i+3]] for i in range(0, len(documents), 3)
]

# Define the layout for the window
layout = [
    [sg.Text('Common Scripts', text_color='black', background_color='white')],
    *buttons_layout,
    [sg.Text('', size=(30, 1), key='-OUTPUT-')],
    [sg.Button('Add Scripts'), sg.Button('Delete Scripts')],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Clipboard App', layout)

# Event loop to process events and get values from elements
while True:
    event, values = window.read()

    # Exit the program if the window is closed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event =='Delete Scripts':
        Delete_Scripts()
        # Update the documents and recreate the button layout
        documents = db.all()
        buttons_layout = [
            [sg.Button(doc.get('name', 'N/A'), key=f'-DOC-{doc.doc_id}-') for doc in documents[i:i+3]] for i in range(0, len(documents), 3)
        ]
        # Update the window with the new layout
        window.close()
        window = sg.Window('Clipboard App', layout=[
            [sg.Text('Common Scripts', text_color='black', background_color='white')],
            *buttons_layout,
            [sg.Text('', size=(30, 1), key='-OUTPUT-')],
            [sg.Button('Add Scripts'), sg.Button('Delete Scripts')],
            [sg.Button('Exit')]
        ])



    if event == 'Add Scripts':
        Add_Scripts()
        # Update the documents and recreate the button layout
        documents = db.all()
        buttons_layout = [
            [sg.Button(doc.get('name', 'N/A'), key=f'-DOC-{doc.doc_id}-') for doc in documents[i:i+3]] for i in range(0, len(documents), 3)
        ]
        # Update the window with the new layout
        window.close()
        window = sg.Window('Clipboard App', layout=[
            [sg.Text('Common Scripts', text_color='black', background_color='white')],
            *buttons_layout,
            [sg.Text('', size=(30, 1), key='-OUTPUT-')],
            [sg.Button('Add Scripts'), sg.Button('Delete Scripts')],
            [sg.Button('Exit')]
        ])

    # Handle the button click events for each document
    for doc in documents:
        button_key = f'-DOC-{doc.doc_id}-'
        if event == button_key:
            # Extract data from the selected document (modify this based on your data structure)
            data = doc.get('data')
            pyperclip.copy(data)
            pyperclip.paste()
            # Update the output text element with the extracted data
            window['-OUTPUT-'].update(f'Copied Script!')

# Close the TinyDB database and the window
db.close()
window.close()

#===========================================================================================================


#================================================================================================================
# Initialize the TinyDB database

