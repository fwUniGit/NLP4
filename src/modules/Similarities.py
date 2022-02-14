from sentence_transformers import SentenceTransformer, util
from AbstractExtraction import get_abstract_by_pdf
from PDFMiner import get_pdf_text
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')


def specter_query_reference_similarity(corpus_set, query_set):
    model = SentenceTransformer('allenai-specter')
    corpus = [paper['title'] + '[SEP]' + paper['abstract'] for paper in corpus_set]

    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    match_set = {}
    for key in query_set:
        if query_set[key]['abstract'] == "None":
            continue
        query = query_set[key]['title'] + '[SEP]' + query_set[key]['abstract']
        query_embeddings = model.encode(query, convert_to_tensor=True)
        match_set[key] = util.semantic_search(query_embeddings, corpus_embeddings)
    return match_set


def specter_1to1_cosine(first, second):
    model = SentenceTransformer('allenai-specter')
    first = model.encode(first, convert_to_tensor=True)
    second = model.encode(second, convert_to_tensor=True)
    return util.cos_sim(first, second)


def pdf_similarity(first, second, only_abstract=False):
    if only_abstract:
        first_abs = get_abstract_by_pdf(first)['abstract']
        second_abs = get_abstract_by_pdf(second)['abstract']
        if first_abs == "None" or second_abs == "None":
            print("Sorry couldn't retrieve the abstracts for both PDFs, try with whole PDF")
        return specter_1to1_cosine(first_abs, second_abs)
    else:
        return specter_1to1_cosine(get_pdf_text(first), get_pdf_text(second))
