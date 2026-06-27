from app.matcher.page_matcher import PageMatcher

matcher = PageMatcher()

pages = [
    "My Applications",
    "Facilities",
    "Tickets",
    "Contact",
    "Announcements",
    "Settings",
    "User Management",
    "FAQs"
]

for page in pages:

    result = matcher.get_page(page)

    print(page)

    if result:

        print("Matched ->", result["title"])

    else:

        print("No Match")

    print()