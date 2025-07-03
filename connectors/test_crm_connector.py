# Dummy CRM connector
# -----------------------------------------------------------------------------
# Purpose
# -------
# Provide stand‑in `fetch_ticket` and `update_ticket` functions so the pipeline
# can be demo‑ed without hitting a real CRM API.
# -----------------------------------------------------------------------------

from schemas import Ticket, RedactedTicket

# In‑memory “database” keyed by ticket_id
_FAKE_DB: dict[int, str] = {
    101: (
        "Hello, my name is Alice Smith. You can reach me at "
        "alice.smith@example.com or +1‑202‑555‑0183. "
        "My SSN is 123‑45‑6789."
    ),
    102: (
        "Customer John Doe called from +1 (415) 555‑2671 on 2025‑06‑15. "
        "He gave card 4111 1111 1111 1111 for the order."
    ),
    103: (
        "Name: Emily Johnson\nEmail: emily.j@example.co.uk\nDOB: 1988-11-02\n"
        "Passport: X12345678"
    ),
    104: (
        "Billing info for Max Lee: card number 5500 0000 0000 0004, "
        "expiry 07/26, CVV 123."
    ),
    105: (
        "User IP 192.168.0.1 accessed the system at 10:45AM. "
        "Associated user: Ahmed Karim, email ahmed.k@domain.org."
    ),
    106: (
        "Client Sarah O'Neil (ID: 567-89-1234) submitted a complaint on "
        "January 10, 2025 via support@business.com."
    ),
    107: (
        "Delivery scheduled to 742 Evergreen Terrace, Springfield, IL. "
        "Contact: homer.simpson@sprmail.com, phone: (333) 444-5566."
    ),
    108: (
        "Meeting notes: Dr. Henry Wong, born 1975-03-22, SSN 987-65-4321. "
        "He mentioned updating bank info: IBAN NL91 ABNA 0417 1643 00."
    ),
    109: (
        "New registration:\nName: Olivia Brown\nPhone: +44 7700 900123\n"
        "Email: olivia_brown123@mail.net\nLicense: D7654321"
    ),
    110: (
        "Incident report for user ID 8899:\nName: Pavel Savvateev\n"
        "Email: p.savvateev@corp.int\nLogged in from IP 203.0.113.5 at 09:12."
    ),
    111: (
        "Student Mia Patel (Date of Birth: 2001-04-18) submitted her "
        "university ID: U20211234 and email: mia.patel@edu.edu."
    ),
}


# ---------------------------------------------------------------------------
# 🎣 fetch_ticket
# ---------------------------------------------------------------------------

def fetch_ticket(source: str, ticket_id: int) -> Ticket:
    """Return a hard‑coded Ticket object for demo purposes."""
    body = _FAKE_DB.get(ticket_id, f"<placeholder body for ticket {ticket_id}>")
    return Ticket(source=source, ticket_id=ticket_id, ticket_body=body)

# ---------------------------------------------------------------------------
# ✏️ update_ticket
# ---------------------------------------------------------------------------

def update_ticket(ticket: RedactedTicket) -> None:
    """Pretend to push the redacted ticket back – just print to console."""
    print("[FAKE_CRM] Updated ticket", ticket.ticket_id)
    print("[FAKE_CRM] Body:", ticket.ticket_body)
