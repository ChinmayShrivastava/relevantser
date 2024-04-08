from typing import List

from llama_index.llms.openai import OpenAI
from urltotext import ContentFinder

from .searchresultsprovider import SERProvider
from .textscore import ComponentItem, Components, TextScore


class RelevantContent:

    def __init__(
        self,
        query: str = None,
        urls: List[str] = None
    ) -> None:
        self.query = query
        self.urls = urls
        self.ser = None
        self.search_performed = False
        self.cf = ContentFinder()
        self.content = {}
        # self.summarizer = TextSummarizer()
        self.llm = OpenAI(model="gpt-3.5-turbo")

    def _get_search_results(self):
        if not self.ser:
            provider = SERProvider(self.query)
            self.ser = provider.get_results()
            return self.ser
        else:
            return self.ser
    
    def add_search_urls(self):
        self._get_search_results()
        self.urls = [result.url for result in self.ser]
    
    def _scrape_urls(self):
        for url in self.urls:
            if url not in self.content:
                self._scrape_url(url)

    def _scrape_url(self, url: str):
        if url not in self.content:
            try:
                text = self.cf.get_article(url)
                if text:
                    components = self.cf.get_components(url)
                    self.content[url] = {
                        "text": text.text,
                        "components": Components(components=[
                            ComponentItem(elementname=elementname, elementtext=elementtext)
                            for elementname, elementtext in components
                        ])
                    }
                else:
                    self.content[url] = {
                        "text": None,
                        "components": None
                    }
            except Exception as e:
                print(e)
                self.content[url] = {
                    "text": None,
                    "components": None
                }
            # self.content[url] = {
            #     "text": self.cf.get_article(url).text 
            #     if self.cf.get_article(url) else None,
            #     "components": Components(components=[
            #         ComponentItem(elementname=elementname, elementtext=elementtext)
            #         for elementname, elementtext in self.cf.get_components(url)
            #     ]) if self.cf.get_components(url) else None,
            # }
    
    def get_score(self):
        if self.urls is None:
            self.add_search_urls()
        self._scrape_urls()
        for url in self.urls:
            text = self.content[url]["text"]
            if text:
                text = text.strip()
                try:
                    score = TextScore(
                        query=self.query, 
                        text=text, 
                        components=self.content[url]["components"],
                        # summarizer=self.summarizer, 
                        llm=self.llm
                    )
                except Exception as e:
                    score = None
            else:
                score = None
            self.content[url]["score"] = score
        # filter urls with no content
        self.content = {url: content for url, content in self.content.items() if content["score"]}
        return self.content

if __name__ == "__main__":
    rc = RelevantContent("Deep learning for generative AI")
    content = rc.get_score()
    # print(content)