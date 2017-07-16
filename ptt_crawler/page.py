class Page:
    def __init__(self, url, links=[]):
        self.url = url
        self.links = links

    def __iter__(self):
        return iter(self.links)
