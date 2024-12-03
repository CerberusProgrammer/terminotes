# Terminotes

Terminotes is a simple note-taking application that runs in the terminal.

## Why Terminotes?

I'm full against the idea of using a note-taking application that requires me to create an account or sign in. I don't want my notes to be stored on a server somewhere. I want them to be stored locally on my machine. That's why I created Terminotes. It's a simple note-taking application that runs in the terminal and stores notes locally on your machine. No need to create an account or sign in.

Also I code on my tablet or phone, and my keyboard is connected, and I need to add a super fast note without opening a browser or an app that requires a lot of resources (And time to open).

So Terminotes is a simple solution for me, and I hope it will be for you too. A very simple terminal app but with the idea of being fast and easy to use.

## MVP

- Create notes with a title and content (body) in the terminal
- List all notes
- View a note by its title
- Delete a note by its title
- Search for notes by title or content
- Export notes to a JSON file
- Import notes from a JSON file
- Configuration file to store the notes file path
- An option to clear all notes
- An option to reset the configuration
- An option to show the configuration
- An option to show the configuration file path
- A help message
- A version message
- A configuration file
- Notes storage in SQLite
- Multiline notes support (Title and content)
- [Required] A CLI
- [Optional] Animation when adding, deleting, or viewing a note (I'm not sure about this one)
- [Optional] A GUI (I'm not sure about this one too)
- [Future] A book to store notes in different categories
- [Future] A reminder system
- [Future] Tags for notes
- [Future] Connection to a cloud service (Like Firebase) to store notes
- [Future] Sync notes between devices
- [Future] Encryption for notes
- [Future] Password protection for notes
- [Future] Markdown support

## MVP Usage

- `terminotes add` to add a note with only content (The title will be the first line of the content)
- `terminotes add -t "Title"` to add a note with a title and no content
- `terminotes add -c "Content"` to add a note with no title and only content
- `terminotes add -t "Title" -c "Content"` to add a note with a title and content
- `terminotes add -m` to add a note with a multiline content (The title will be the first line of the content) (The content will be added line by line until you type `[end]` in a new line)
- `terminotes add -t "Title" -m` to add a note with a title and multiline content (The content will be added line by line until you type `[end]` in a new line)
- `terminotes add -c "Content" -m` to add a note with no title and multiline content (The content will be added line by line until you type `[end]` in a new line)
- `terminotes add -t "Title" -c "Content" -m` to add a note with a title, content, and multiline content (The content will be added line by line until you type `[end]` in a new line)
- `terminotes list` to list all notes
- `terminotes list -M` to list all notes with their titles only
- `terminotes list -C` to list all notes with their content only
- `terminotes list -T` to list all notes with their titles and content
- `terminotes list -t "Title"` to list a note by its title
- `terminotes list -c "Content"` to list a note by its content
- `terminotes list -q "Query"` to list notes by title or content
- `terminotes list -D` to list all notes with their titles and content in a detailed view
- `terminotes list -D -t "Title"` to list a note by its title in a detailed view
- `terminotes list -D -c "Content"` to list a note by its content in a detailed view
- `terminotes list -D -q "Query"` to list notes by title or content in a detailed view
- `terminotes list -d` to list all notes with their date of creation
- `terminotes list -d -t "Title"` to list a note by its title with its date of creation
- `terminotes list -d -c "Content"` to list a note by its content with its date of creation
- `terminotes list -d -q "Query"` to list notes by title or content with their date of creation
- `terminotes list -D -d` to list all notes with their titles, content, and date of creation in a detailed view
- `terminotes list -D -d -t "Title"` to list a note by its title with its content and date of creation in a detailed view
- `terminotes list -D -d -c "Content"` to list a note by its content with its title and date of creation in a detailed view
- `terminotes list -D -d -q "Query"` to list notes by title or content with their content and date of creation in a detailed view
- `terminotes list -d -D` to list all notes with their date of creation in a detailed view
- `terminotes list -d -D -t "Title"` to list a note by its title with its date of creation in a detailed view
- `terminotes list -d -D -c "Content"` to list a note by its content with its date of creation in a detailed view
- `terminotes list -d -D -q "Query"` to list notes by title or content with their date of creation in a detailed view
- `terminotes list -M -C` to list all notes with their titles and content only
- `terminotes list -M -C -t "Title"` to list a note by its title with its content only
- `terminotes list -M -C -c "Content"` to list a note by its content with its title only
- `terminotes list -M -C -q "Query"` to list notes by title or content with their content and title only
- `terminotes list -M -C -D` to list all notes with their titles and content in a detailed view
- `terminotes list -M -C -D -t "Title"` to list a note by its title with its content in a detailed view
- `terminotes list -M -C -D -c "Content"` to list a note by its content with its title in a detailed view
- `terminotes list -M -C -D -q "Query"` to list notes by title or content with their content and title in a detailed view
- `terminotes list -M -C -d` to list all notes with their titles and content with their date of creation
- `terminotes list -M -C -d -t "Title"` to list a note by its title with its content and date of creation
- `terminotes view -t "Title"` to view a note by its title
- `terminotes view -s "Title"` to search for a note by its title or content or date of creation and view it (A cursor selection will be shown to select the note if there are multiple notes with the same title) (The search query will be highlighted in the note)
- `terminotes delete -t "Title"` to delete a note by its title (A cursor selection will be shown to select the note if there are multiple notes with the same title)
- `terminotes search -q "Query"` to search for notes by title or content
- `terminotes help` to show the help message
- `terminotes version` to show the version of Terminotes
- `terminotes clear` to clear all notes
- `terminotes export` to export all notes to a JSON file
- `terminotes import` to import notes from a JSON file
- `terminotes config` to configure Terminotes
- `terminotes config -r` to reset the configuration
- `terminotes config -l` to show the configuration
- `terminotes config -s` to show the configuration file path
