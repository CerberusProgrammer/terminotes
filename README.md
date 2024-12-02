# Terminotes

Terminotes is a simple note-taking application that runs in the terminal. It is written in Dart and uses the `dart:io` library to interact with the terminal.

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

## MVP Usage

- `terminotes add` to add a note with only content (The title will be the first line of the content)
- `terminotes add -t "Title" -c "Content"` to add a note with a title and content
- `terminotes list` to list all notes
- `terminotes view -t "Title"` to view a note by its title
- `terminotes delete -t "Title"` to delete a note by its title
- `terminotes search -q "Query"` to search for notes by title or content
