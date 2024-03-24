COMPREHENSIVE_CHECK = """As an advanced language model, your task is to analyze the texe attached and rate it on a scale of 1-10 based on how comprehensive it is.
The text is a summary of a longer article, and we want to know if based on the summary, the larger article is comprehensive. The comprehensiveness is based on the text's main topic of focus.
Summary Text:
{summary}
---
Rate the text on a scale of 1-10 based on how comprehensive it is.
1 - not comprehensive at all
5 - somewhat comprehensive
10 - very comprehensive, include most of the important details
Reply with just the number.
Rating:"""

RELEVANCE_CHECK = """As an advanced language model, your task is to analyze the text attached and rate it on a scale of 1-10 based on how relevant it is to the query.
The text is a summary of a longer article, and we want to know if based on the summary, the text is relevant to the query. The relevance is based on the text's main topic of focus.
Summary Text:
{summary}
---
Query:
{query}
---
Rate the text on a scale of 1-10 based on how relevant it is to the query.
1 - not relevant at all
5 - somewhat relevant
10 - very relevant, includes most of the important details
Reply with just the number.
Rating:"""