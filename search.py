from duckduckgo_search import DDGS

def search_duckduckgo(query, max_results=3):
    try:
        results = DDGS().text(query, max_results=max_results)
        return results
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []
