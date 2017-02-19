from summa import summarizer


def corpus(corpus):
  """
  Get a summary of the corpus
  :param corpus:
  :return:
  """
  return summarizer.summarize(corpus, words=280)
