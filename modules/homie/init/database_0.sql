PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS DEVICE (
    device    TEXT NOT NULL,
    node      TEXT NOT NULL,
    property  TEXT NOT NULL,
    updatedAt DATE,
    PRIMARY KEY(device, node, property)
);

CREATE TABLE IF NOT EXISTS WIDGET (
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    device   TEXT NOT NULL,
    node     TEXT NOT NULL,
    property TEXT NOT NULL,
    label    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PAGE (
    id    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT NOT NULL,
    label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PAGE_WIDGET (
  id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
  page   INTEGER,
  widget INTEGER,
  FOREIGN KEY(page) REFERENCES Page(id),
  FOREIGN KEY(widget) REFERENCES Widget(id)
);