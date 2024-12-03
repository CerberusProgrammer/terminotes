import sqlite3
import argparse
import os
import uuid as uuid_lib
from datetime import datetime
import json
import curses

db_file = 'notes.db'
config_file = 'config.json'
db_exists = os.path.exists(db_file)

conn = sqlite3.connect(db_file)
c = conn.cursor()

if not db_exists:
    c.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL
    )
    ''')
    conn.commit()

class Note:
    def __init__(self, title, content, note_uuid=None, created_at=None, updated_at=None):
        self.uuid = note_uuid or str(uuid_lib.uuid4())
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

def add_note(title, content):
    note = Note(title, content)
    c.execute('INSERT INTO notes (uuid, title, content, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)', 
              (note.uuid, note.title, note.content, note.created_at, note.updated_at))
    conn.commit()
    print("Note added.")

def list_notes(order_by='createdAt'):
    c.execute(f'SELECT title, uuid, createdAt FROM notes ORDER BY {order_by}')
    notes = c.fetchall()
    for note in notes:
        print(f'{note[0]} ({note[1]}) - Created at: {note[2]}')

def view_note(search_term):
    c.execute('SELECT title, uuid, createdAt FROM notes WHERE title LIKE ? OR content LIKE ? OR createdAt LIKE ?', 
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    notes = c.fetchall()
    if not notes:
        print("No notes found.")
        return

    def display_menu(stdscr):
        curses.curs_set(0)
        current_row = 0

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            for idx, note in enumerate(notes):
                x = w//2 - len(note[0])//2
                y = h//2 - len(notes)//2 + idx
                if idx == current_row:
                    stdscr.addstr(y, x, f'> {note[0]} ({note[1]}) - Created at: {note[2]}')
                else:
                    stdscr.addstr(y, x, f'  {note[0]} ({note[1]}) - Created at: {note[2]}')

            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(notes) - 1:
                current_row += 1
            elif key == ord('w') and current_row > 0:
                current_row -= 1
            elif key == ord('s') and current_row < len(notes) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return notes[current_row]

    selected_note = curses.wrapper(display_menu)
    if selected_note:
        c.execute('SELECT content FROM notes WHERE uuid = ?', (selected_note[1],))
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

def export_notes(file_path):
    c.execute('SELECT uuid, title, content, createdAt, updatedAt FROM notes')
    notes = c.fetchall()
    notes_list = [{'uuid': note[0], 'title': note[1], 'content': note[2], 'createdAt': note[3], 'updatedAt': note[4]} for note in notes]
    with open(file_path, 'w') as f:
        json.dump(notes_list, f, indent=4)
    print(f"Notes exported to {file_path}")

def import_notes(file_path):
    with open(file_path, 'r') as f:
        notes_list = json.load(f)
    for note in notes_list:
        c.execute('INSERT INTO notes (uuid, title, content, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)', 
                  (note['uuid'], note['title'], note['content'], note['createdAt'], note['updatedAt']))
    conn.commit()
    print(f"Notes imported from {file_path}")

def clear_notes():
    c.execute('DELETE FROM notes')
    conn.commit()
    print("All notes cleared.")

def reset_config():
    if os.path.exists(config_file):
        os.remove(config_file)
    print("Configuration reset.")

def show_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(json.dumps(config, indent=4))
    else:
        print("No configuration found.")

def show_config_path():
    print(f"Configuration file path: {os.path.abspath(config_file)}")

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def main():
    parser = argparse.ArgumentParser(description='Terminotes: A terminal-based note-taking application')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new note')
    add_parser.add_argument('-t', '--title', type=str, help='The title of the note')
    add_parser.add_argument('-c', '--content', type=str, help='The content of the note')
    add_parser.add_argument('-m', '--multiline', action='store_true', help='Add multiline content')

    list_parser = subparsers.add_parser('list', help='List all notes')
    list_parser.add_argument('-o', '--order', type=str, choices=['createdAt', 'updatedAt'], default='createdAt', help='Order by field')

    view_parser = subparsers.add_parser('view', help='View a note')
    view_parser.add_argument('-s', '--search', type=str, required=True, help='The search term')

    delete_parser = subparsers.add_parser('delete', help='Delete a note by its title')
    delete_parser.add_argument('-t', '--title', type=str, required=True, help='The title of the note')

    search_parser = subparsers.add_parser('search', help='Search notes by title or content')
    search_parser.add_argument('-q', '--query', type=str, required=True, help='The search query')

    export_parser = subparsers.add_parser('export', help='Export notes to a JSON file')
    export_parser.add_argument('-f', '--file', type=str, required=True, help='The file path to export notes')

    import_parser = subparsers.add_parser('import', help='Import notes from a JSON file')
    import_parser.add_argument('-f', '--file', type=str, required=True, help='The file path to import notes from')

    subparsers.add_parser('clear', help='Clear all notes')

    config_parser = subparsers.add_parser('config', help='Configure Terminotes')
    config_parser.add_argument('-r', '--reset', action='store_true', help='Reset the configuration')
    config_parser.add_argument('-l', '--list', action='store_true', help='Show the configuration')
    config_parser.add_argument('-s', '--show-path', action='store_true', help='Show the configuration file path')

    subparsers.add_parser('help', help='Show the help message')
    subparsers.add_parser('version', help='Show the version of Terminotes')

    args = parser.parse_args()

    if args.command == 'add':
        if args.multiline:
            print("Enter the content line by line. Type '[end]' on a new line to finish.")
            lines = []
            while True:
                line = input()
                if line == '[end]':
                    break
                lines.append(line)
            content = '\n'.join(lines)
        else:
            content = args.content
        title = args.title if args.title else content.split('\n')[0]
        add_note(title, content)
    elif args.command == 'list':
        list_notes(args.order)
    elif args.command == 'view':
        view_note(args.search)
    elif args.command == 'delete':
        delete_note(args.title)
    elif args.command == 'search':
        search_notes(args.query)
    elif args.command == 'export':
        export_notes(args.file)
    elif args.command == 'import':
        import_notes(args.file)
    elif args.command == 'clear':
        clear_notes()
    elif args.command == 'config':
        if args.reset:
            reset_config()
        elif args.list:
            show_config()
        elif args.show_path:
            show_config_path()
    elif args.command == 'help':
        parser.print_help()
    elif args.command == 'version':
        print("Terminotes version 1.0")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    conn.close()