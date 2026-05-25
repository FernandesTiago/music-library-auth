# Music Library & Auth System (CLI)

A terminal-based music library manager with user authentication and
role-based access control. Built as a hands-on deep-dive into Python
classes, SQLite, and secure credential handling.

## What it does

- Stores a music library (song, album, artist, rating) in SQLite with
  full CRUD operations.
- Handles user signup and login, with passwords hashed using bcrypt —
  credentials are never stored as plain text.
- Enforces role-based access: admins have full control, while standard
  users can list and search only.

## Architecture

Three classes, each with a single responsibility:

- `DataBase` — music CRUD against the `musics` table.
- `UserDataBase` — user creation and authentication against the `users`
  table.
- `Menu` — application flow, screen rendering, and access control.

Two independent SQLite tables (`musics`, `users`) keep data and auth
concerns separated.

## Access control

Roles are assigned without any hardcoded credentials in the source:

- The **first user** to sign up becomes the **owner/admin**. This is the
  one-time bootstrap pattern used by many self-hosted tools (the first
  account during setup owns the system).
- Every subsequent signup is a **standard user**.
- Privilege is granted downward, never claimed: a standard user cannot
  self-select an admin role.

This avoids the common anti-pattern of a magic admin password embedded
in the code, which would leak through version control and can't be
rotated.

## Running

```bash
python MLA.py
```

Requires Python 3 and `bcrypt` (`pip install bcrypt`). The SQLite
database file is created automatically on first run.

## Status

Functional. Core features — music CRUD, bcrypt authentication, and
role-based gating — are implemented and working.

## Planned improvements

- **User management tab** — an admin-only screen to view users and
  promote/demote between roles.
- **Protected owner account** — only the first admin (owner) can demote
  other admins, and cannot demote or remove their own account. This
  prevents admin-lockout scenarios.
- **Explicit owner flag** — store ownership as a dedicated column rather
  than inferring it from user ID.
- **Input/UX hardening** — clearer error messages and validation polish.

## Background

This started as a learning exercise focused on combining Python classes
with SQLite and bcrypt password hashing. The original goal was the OOP
structure and secure password *storage*, not a hardened admin system —
so the first version assigned the admin role with a simple hardcoded
check just to get a privileged user into the flow.

That hardcoded approach is a known security flaw: secrets in source code
leak through version control and can't be rotated. I'm reworking the
role assignment to remove it entirely — the first registered user
becomes the owner/admin (a standard bootstrap pattern), and roles are
managed from an admin-only tab rather than claimed at signup. The notes
below track that work.
