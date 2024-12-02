import sqlite3
import argparse

# Conectar a la base de datos SQLite
conn = sqlite3.connect('notes.db')
c = conn.cursor()

# Crear la tabla de notas si no existe
c.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')
conn.commit()

def add_note(title, content):
    c.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    print("Nota agregada.")

def list_notes():
    c.execute('SELECT title FROM notes')
    notes = c.fetchall()
    for note in notes:
        print(note[0])

def view_note(title):
    c.execute('SELECT content FROM notes WHERE title = ?', (title,))
    note = c.fetchone()
    if note:
        print(note[0])
    else:
        print("Nota no encontrada.")

def delete_note(title):
    c.execute('DELETE FROM notes WHERE title = ?', (title,))
    conn.commit()
    print("Nota eliminada.")

def search_notes(query):
    c.execute('SELECT title, content FROM notes WHERE title LIKE ? OR content LIKE ?', (f'%{query}%', f'%{query}%'))
    notes = c.fetchall()
    for note in notes:
        print(f'Title: {note[0]}')
        print(f'Content: {note[1]}')
        print('---')

def main():
    parser = argparse.ArgumentParser(description='Terminotes: Una aplicación de notas en la terminal')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Agregar una nueva nota')
    add_parser.add_argument('-t', '--title', type=str, help='El título de la nota')
    add_parser.add_argument('-c', '--content', type=str, required=True, help='El contenido de la nota')

    subparsers.add_parser('list', help='Listar todas las notas')

    view_parser = subparsers.add_parser('view', help='Ver una nota por su título')
    view_parser.add_argument('-t', '--title', type=str, required=True, help='El título de la nota')

    delete_parser = subparsers.add_parser('delete', help='Eliminar una nota por su título')
    delete_parser.add_argument('-t', '--title', type=str, required=True, help='El título de la nota')

    search_parser = subparsers.add_parser('search', help='Buscar notas por título o contenido')
    search_parser.add_argument('-q', '--query', type=str, required=True, help='La consulta de búsqueda')

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