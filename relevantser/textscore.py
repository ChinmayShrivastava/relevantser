from typing import List

import readability
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel

from prompts import COMPREHENSIVE_CHECK, RELEVANCE_CHECK

load_dotenv()


def score_type_dispatch(obj, score_type):
    if score_type == 'FleschReadingEase':
        return obj.redability_score('FleschReadingEase')
    elif score_type == 'ComprehensiveScore':
        return obj.llm_comprehensive_score()
    elif score_type == 'RelevanceScore':
        return obj.query_relevance_score()
    elif score_type == 'PersonalizedScore':
        return obj.personalized_score()
    else:
        raise ValueError("Invalid score type")
    
class ComponentItem(BaseModel):
    elementname: str
    elementtext: str

class Components(BaseModel):
    components: List[ComponentItem]

class TextScore:

    def __init__(
        self,
        query: str,
        text: str,
        components: Components = None,
        score_types: List[str] = ["FleschReadingEase", "ComprehensiveScore", "RelevanceScore"],
        # summarizer: TextSummarizer = TextSummarizer(),
        llm: OpenAI = OpenAI(model="gpt-3.5-turbo"),
    ) -> None:
        self.query = query
        self.text = text
        self.components = components
        self.score_types = score_types
        # self.summarizer = summarizer
        self.summary = None
        self.llm = llm
        self.scores = {score_type: score_type_dispatch(self, score_type) for score_type in score_types}

    def __str__(self):
        return str(self.scores)

    def redability_score(self, score_type):
        return readability.getmeasures(self.text, lang='en')['readability grades'][score_type]
    
    def llm_comprehensive_score(self):
        # measures whether the text is comprehensive enough to answer the query and more
        # instead of the summary, we can also just use the headings. (we can sau if headings aren't enough, then we can use the summary.)
        if self.summary is None:
            # self.summary = self.summarizer(self.text)
            self.summary = self.extract_headings()
        res = int(self.llm.complete(COMPREHENSIVE_CHECK.format(summary=self.summary)).text)
        return res

    def query_relevance_score(self):
        # measures how well the text captures the answer to the query
        if self.summary is None:
            # self.summary = self.summarizer(self.text)
            self.summary = self.extract_headings()
        res = int(self.llm.complete(RELEVANCE_CHECK.format(summary=self.summary, query=self.query)).text)
        return res

    def personalized_score(self):
        # measures the text's ability to be effective to the user given their knowledge base
        pass

    def extract_headings(self):
        accepted_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        headings = []
        for component in self.components.components:
            if component.elementname in accepted_tags:
                headings.append(component.elementtext)
        return "\n".join(headings)


# if __name__ == "__main__":
#     body = """In the last two decades, automatic extractive text
# summarization on lectures has demonstrated to be a useful
# tool for collecting key phrases and sentences that best
# represent the content. However, many current approaches
# utilize dated approaches, producing sub-par outputs or
# requiring several hours of manual tuning to produce
# meaningful results. Recently, new machine learning
# architectures have provided mechanisms for extractive
# summarization through the clustering of output embeddings
# from deep learning models. This paper reports on the project
# called “lecture summarization service”, a python-based
# RESTful service that utilizes the BERT model for text
# embeddings and K-Means clustering to identify sentences
# closest to the centroid for summary selection. The purpose of
# the service was to provide student’s a utility that could
# summarize lecture content, based on their desired number of
# sentences. On top of summary work, the service also
# includes lecture and summary management, storing content
# on the cloud which can be used for collaboration. While the
# results of utilizing BERT for extractive text summarization
# were promising, there were still areas where the model
# struggled, providing future research opportunities for further
# improvement. All code and results can be found here:"""
#     scores = TextScore("What is the purpose of the service?", body)
#     # readability score
#     print(scores.scores)