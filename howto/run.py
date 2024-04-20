from relevantser.scraper import RelevantContent
import asyncio
import time

rc = RelevantContent("Deep learning for generative AI")
start = time.time()
# content = rc.get_score()
# print(content) # Time taken: 27.448663234710693 seconds
content = asyncio.run(rc.async_get_score())
print(content)
print(f"Time taken: {time.time() - start} seconds")