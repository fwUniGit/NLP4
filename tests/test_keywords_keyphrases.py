import arxiv
from src.modules.KeywordKeyphraseExtractor import yake_extraction, rake_phrase_extraction
import nltk
nltk.download('all')


def test_paper_selection():
    pdf = ''
    search = arxiv.Search(query="nlp keyword extraction", max_results=1, sort_by=arxiv.SortCriterion.Relevance)
    for result in search.results():
        pdf = result.summary
    rake = rake_phrase_extraction(pdf)
    yake = yake_extraction(pdf)
    assert isinstance(rake, list)
    assert isinstance(yake, list)
