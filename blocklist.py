"""
blocklist.py

This file just contains the blocklist(logged out tokens) of the JWT tokens. It will be imported by
the app and the logout resource so that tokens can be added to the blocklist
when the user logs out.
"""
# Ideally, this data should be stored in a db or redis cache for security, quick
# lookups and other bennefits, can be improved later, or submit a PR if you'd
# like to help out...
BLOCKLIST = set()
