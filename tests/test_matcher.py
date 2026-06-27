from app.matcher.page_matcher import PageMatcher

matcher = PageMatcher()

page = matcher.get_page("My Applications")

print(page)