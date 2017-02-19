from multiprocessing.pool import ThreadPool
from summa import keywords
import search_word
import spacy


nlp = spacy.load("en")
thread_pool = ThreadPool(4)


def _keywords_(corpus):
  """
  Find important keywords - use TextRank algorithm to find
  most important keywords, then a fuzzier/dumber match with
  NER tagging
  :param corpus:
  :return:
  """
  keywords_list = keywords.keywords(corpus).split("\n")

  def label_normalizer(spacy_label):
    label = {
      "PERSON": "Person",
      "NORP": "Nationality/Religious/Political Groups",
      "FACILITY": "Facility",
      "ORG": "Organization",
      "GPE": "Geographic Location",
      "LOC": "Location",
      "PRODUCT": "Thing",
      "EVENT": "Event",
      "WORK_OF_ART": "Art",
      "LANGUAGE": "Language",
    }
    return label.get(spacy_label, spacy_label.title())
  entity_tuples = [
    (label_normalizer(entity.label_), entity.text)
    for entity in nlp(corpus).ents
  ]

  if len(keywords_list) >= 2:
    '''
    If keyword in keywords_list fuzzy match with a keyword in NER
    generated list, do a transform to obtain that NER's provided
    entity category
    '''
    def transformer(keyword):
      for (entity_category, entity_text) in entity_tuples:
        if keyword.lower() in entity_text.lower():
          return entity_category, keyword
        if entity_text.lower() in keyword.lower():
          return entity_category, keyword

      return "", keyword
    return map(transformer, keywords_list)

  return entity_tuples


def _map_info_thread_((label, word)):
  results_list = search_word.search_word(word)

  def transformer(result):
    if label:
      result["entity"] = label
    return result
  results_list = map(transformer, results_list)
  return results_list


def sentence(sentence):
  """
  Get cards of information based on important concepts on a sentence
  :param sentence:
  :return: [{topic, shortDescription, description, entity, imgUrl}]
  """
  keywords_list = _keywords_(corpus)

  cards = thread_pool.map(
    _map_info_thread_,
    keywords_list
  )
  thread_pool.close()
  thread_pool.join()

  return [item for sublist in cards for item in sublist]


def corpus(corpus):
  """
  Get cards of information based on important concepts on a corpus
  :param corpus:
  :return: [{topic, shortDescription, description, entity, imgUrl}]
  """
  keywords_list = _keywords_(corpus)

  cards = thread_pool.map(
    _map_info_thread_,
    keywords_list
  )
  thread_pool.close()
  thread_pool.join()

  return [item for sublist in cards for item in sublist]
