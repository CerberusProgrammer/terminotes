import sqlite3
import argparse
import os
import uuid as uuid_lib

db_file = 'notes.db'
db_exists = os.path.exists(db_file)

conn = sqlite3.connect(db_file)
c = conn.cursor()

if not db_exists:
    c.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    ''')
    conn.commit()

class Note:
    def __init__(self, title, content, note_uuid=None):
        self.uuid = note_uuid or str(uuid_lib.uuid4())
        self.title = title
        self.content = content

def add_note(title, content):
    note = Note(title, content)
    c.execute('INSERT INTO notes (uuid, title, content) VALUES (?, ?, ?)', (note.uuid, note.title, note.content))
    conn.commit()
    print("Note added.")

def list_notes():
    c.execute('SELECT title, uuid FROM notes')
    notes = c.fetchall()
    for note in notes:
        print(f'{note[0]} ({note[1]})')

def view_note(title):
    c.execute('SELECT content FROM notes WHERE title = ?', (title,))
    note = c.fetchone()
    if note:
        print(note[0])
    else:
        print("Note not found.")

def delete_note(title):
    c.execute('DELETE FROM notes WHERE title = ?', (title,))
    conn.commit()
    print("Note deleted.")

def search_notes(query):
    c.execute('SELECT title, content FROM notes WHERE title LIKE ? OR content LIKE ?', (f'%{query}%', f'%{query}%'))
    notes = c.fetchall()
    for note in notes:
        print(f'Title: {note[0]}')
        print(f'Content: {note[1]}')
        print('---')

def main():
    parser = argparse.ArgumentParser(description='Terminotes: A terminal-based note-taking application')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new note')
    add_parser.add_argument('-t', '--title', type=str, help='The title of the note')
    add_parser.add_argument('-c', '--content', type=str, required=True, help='The content of the note')

    subparsers.add_parser('list', help='List all notes')

    view_parser = subparsers.add_parser('view', help='View a note by its title')
    view_parser.add_argument('-t', '--title', type=str, required=True, help='The title of the note')

    delete_parser = subparsers.add_parser('delete', help='Delete a note by its title')
    delete_parser.add_argument('-t', '--title', type=str, required=True, help='The title of the note')

    search_parser = subparsers.add_parser('search', help='Search notes by title or content')
    search_parser.add_argument('-q', '--query', type=str, required=True, help='The search query')

    args = parser.parse_args()

    if args.command == 'add':
        title = args.title if args.title else args.content.split('\n')[0]
        add_note(title, args.content)
    elif args.command == 'list':
        list_notes()
    elif args.command == 'view':
        view_note(args.title)
    elif args.command == 'delete':
        delete_note(args.title)
    elif args.command == 'search':
        search_notes(args.query)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    conn.close()