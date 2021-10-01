"""Amazing (Regular) Expressions"""
import re

# Identify a "fun fact"
funfact_regex = re.compile(r'^fun fact\b', re.IGNORECASE)
# Identify a potential Devon mention
devon_regex = re.compile(r'.*devon\b', re.IGNORECASE)
# Meme about socks
sock_regex = re.compile(r'.*sock(puppet)?', re.IGNORECASE)
# Identify the "new member" embed message
new_member_regex = re.compile(r'.*Have fun, and talk to you soon!', re.IGNORECASE)
