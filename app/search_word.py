from os import environ
from multiprocessing.pool import ThreadPool
import requests
import wikipedia
from segtok import segmenter


def knowledge_graph_api(word):
  service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
  request_object = requests.get(service_url, params={
    'query': word,
    'limit': 2,
    'indent': False,
    'key': environ.get("GK_API_KEY")
  })
  results_body = request_object.json()

  if "itemListElement" not in results_body.keys():
    raise RuntimeError("No results found")

  def transform(search_result):
    result_body = search_result.get("result", {})

    topic = result_body.get("name", "")
    shortDescription = result_body.get("description", "")
    description = result_body \
        .get("detailedDescription", {}) \
        .get("articleBody", "")
    entity = result_body \
        .get("@type", ["Unclassified"])[0]
    imgUrl = result_body \
        .get("image", {}) \
        .get("contentUrl", "")

    return {
      'topic': topic,
      'shortDescription': shortDescription,
      'description': description,
      'entity': entity,
      'imgUrl': imgUrl,
      'source': 'KnowledgeGraph'
    }

  return map(transform, results_body.get("itemListElement", []))


def wikipedia_api(word):
  try:
    wikipediaPage = wikipedia.page(word)
  except wikipedia.exceptions.DisambiguationError as e:
    if len(e.options) == 0:
      return []
    else:
      wikipediaPage = wikipedia.page(e.options[0])

  sentence_list = list(segmenter.split_single(
    wikipediaPage.summary
  ))

  topic = wikipediaPage.title
  shortDescription = sentence_list[0]
  description = "".join(sentence_list[0:3])
  entity = ""
  imgUrl = wikipediaPage.images.pop()

  return [{
    'topic': topic,
    'shortDescription': shortDescription,
    'description': description,
    'entity': entity,
    'imgUrl': imgUrl,
    'source': 'Wikipedia'
  }]


def search_word(word):
  """
  Search for a definition/explanation of the word
  :param word:
  :return: [{topic, shortDescription, description, entity, imgUrl}]
  """
  thread_pool = ThreadPool(2)
  answer1 = thread_pool.apply_async(
    func=wikipedia_api, args=(word,)
  )
  answer2 = thread_pool.apply_async(
    func=knowledge_graph_api, args=(word,)
  )
  thread_pool.close()
  thread_pool.join()

  return answer1.get() + answer2.get()
