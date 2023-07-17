import re

def find_urls(text):
    # The regular expression to find URLs
    url_pattern = re.compile(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|\/|\/\/)?[A-z0-9_-]*?[:]?[A-z0-9_-]*?[@]?[A-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?\n')

    # Find all matches of the pattern in the text
    urls = url_pattern.findall(text)
    print(url_pattern.search(text))

    return urls

# Example usage:
text_to_search = "Check out this link: https://www.example.com! And another one: http://subdomain.example.com/page\n"
found_urls = find_urls(text_to_search)
print(found_urls)