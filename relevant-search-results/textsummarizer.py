# from summarizer import Summarizer

# class TextSummarizer:
#     def __init__(
#         self, 
#         min_len: int = 60,
#     ) -> None:
#         self.model = Summarizer()
#         self.min_len = min_len

#     def __str__(self) -> str:
#         return f"{self.model(self.text, min_length=self.min_len)}"
    
#     def __call__(self, text: str) -> str:
#         return self.model(text, min_length=self.min_len)