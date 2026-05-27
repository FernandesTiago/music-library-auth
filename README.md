# Music Library & Auth System (CLI)

A terminal-based music library manager with user authentication and
role-based access control. Built as a hands-on deep-dive into Python
classes, SQLite, and secure credential handling.

## What it does

- Stores a music library (song, album, artist, rating) in SQLite with
  full CRUD operations.
- Handles user signup and login, with passwords hashed using bcrypt —
  credentials are never stored as plain text.
- Enforces a three-tier role system that gates what each user can do.

## Roles & access control

| Role        | Permissions                                          |
| ----------- | ---------------------------------------------------- |
| Common      | List and view songs                                  |
| Admin       | Full song CRUD, plus promote common users to admin   |
| Super Admin | Everything an admin can do, plus demote other admins |

Roles are assigned without any hardcoded credentials in the source:

- The **first user** to sign up becomes the **Super Admin** — the
  one-time bootstrap pattern used by many self-hosted tools.
- Every subsequent signup is a **common** user.
- Privilege is granted downward: a user cannot self-select a role at
  signup. Promotion and demotion happen through an admin-only screen.
- Built-in guards prevent admin lockout: no user can promote or demote
  themselves, and the Super Admin cannot be demoted by anyone.

## Architecture

Three classes, each with a single responsibility:

- `DataBase` — music CRUD against the `musics` table.
- `UserDataBase` — user creation, authentication, and role updates
  against the `users` table.
- `Menu` — application flow, screen rendering, and access control.

## Background

This started as a learning exercise focused on combining Python classes
with SQLite and bcrypt password hashing. The original version assigned
the admin role with a hardcoded password check just to get a privileged
user into the flow — a known security flaw, since secrets in source code
leak through version control and can't be rotated.

I've since removed that entirely. Role assignment now uses the
first-user-becomes-Super-Admin bootstrap pattern, and all further role
changes go through an admin-only management screen with guards against
self-modification and Super Admin demotion.

## Running

```bash
pip install bcrypt
python MLA.py
```

Requires Python 3. The SQLite database is created automatically on first
run. The first account you create becomes the Super Admin.

## Status

Functional. Music CRUD, bcrypt authentication, and the three-tier
role system are all implemented and working.

## Planned improvements

- **Refactor navigation into a single driver loop** — screens currently
  call each other directly rather than returning control to a central
  router, which deepens the call stack on each login/logout cycle.
- **Input/UX hardening** — clearer validation and error messaging.