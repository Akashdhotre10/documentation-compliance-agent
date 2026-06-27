from app.matcher.page_matcher import PageMatcher

matcher = PageMatcher()

pages = [
    "My Applications",
    "Facilities",
    "Action Items",
    "User Management",
    "Announcements",
    "Settings",
    "FAQs",
    "Tickets",
    "Contact"
]

for page in pages:
    print("\n---------------------")
    print(page)
    print("---------------------")

    result = matcher.match(page)

    print(result)