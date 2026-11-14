"""Seat reservation system for a small cinema.

Reserves and releases seats per show, generates ticket codes and
saves/loads the seating plan to a JSON file.
"""

import hashlib
import json
import os

shows = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def _valid_seat(show_id, seat_number):
    """Return True if the show exists and the seat is an int in range."""
    if show_id not in shows:
        return False
    if not isinstance(seat_number, int) or isinstance(seat_number, bool):
        return False
    return 1 <= seat_number <= shows[show_id]["seats"]


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a seat for a show. Returns True on success."""
    if system_logs is None:
        system_logs = []
    if not _valid_seat(show_id, seat_number):
        system_logs.append(f"Invalid seat {seat_number!r} for {show_id}")
        return False
    show = shows[show_id]
    if seat_number in show["booked"]:
        system_logs.append(f"Seat {seat_number} already taken for {show_id}")
        return False
    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a booked seat. Returns True if it was booked."""
    try:
        shows[show_id]["booked"].remove(seat_number)
    except (KeyError, ValueError):
        return False
    return True


def ticket_code(show_id, seat_number):
    """Return a short ticket code for a show/seat pair."""
    raw = (show_id + str(seat_number)).encode()
    return hashlib.sha256(raw).hexdigest()[:8]


def dump_reservations(file="seats.json"):
    """Save all shows to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(shows, f)


def load_reservations(file="seats.json"):
    """Load shows from a JSON file, replacing current state in place."""
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    shows.clear()
    shows.update(data)


def print_seating_summary():
    """Print free seats and bookings for every show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(f"{show['title']}: {free} seats free, "
              f"booked = {show['booked']}")


def main():
    """Run a short demo of the reservation system."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    reserve_seat("SHOW-2", "A7", logs)
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))
    choice = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    try:
        reserve_seat("SHOW-2", int(choice), logs)
    except ValueError:
        logs.append(f"Not a number: {choice!r}")
    for line in logs:
        print(line)
    dump_reservations()
    os.chmod("seats.json", 0o600)
    load_reservations()
    print_seating_summary()


if __name__ == "__main__":
    main()
