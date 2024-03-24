from typing import List

from googlesearch import search


class SEResult:
    def __init__(
        self, 
        url: str,
        title: str,
        description: str
    ) -> None:
        self.url = url
        self.title = title
        self.description = description

class SERProvider:
    def __init__(
        self, 
        query: str,
        results: List[SEResult] = []
    ) -> None:
        self.query = query
        self.results = results

    def _get_results_google(self):
        _results = search(self.query, num_results=10, lang="en", advanced=True)
        for result in _results:
            self.results.append(SEResult(
                url=result.url,
                title=result.title,
                description=result.description
            ))

    def get_results(self):
        self._get_results_google()
        return self.results

    def __iter__(self):
        return iter(self.results)