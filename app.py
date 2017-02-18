from flask import Flask, json, request
from os import environ
from app import info_cards, search_word, summary


app = Flask(__name__)


def response_maker(function):
  """
  Constructs an HTTP response based on the execution of
  the function
  :param function: {func} Function to execute
  :return: {Flask.ResponseObject}
  """
  try:
    result = function()
  except BaseException as e:
    return json.jsonify(
      status=400,
      message=e.message,
      data=dict()
    )

  return json.jsonify(
    status=200,
    message="Success",
    data=result
  )


@app.route('/', methods=["POST"])
def api_entrypoint():
  return json.jsonify(
    status=200,
    message="microservice:nlp",
    data=dict()
  )


@app.route('/cards/sentence', methods=["POST"])
def api_cards_sentence():
  sentence = request.get_json(force=True, silent=True)
  return response_maker(info_cards.sentence(sentence))


@app.route('/cards/corpus', methods=["POST"])
def api_cards_corpus():
  corpus = request.get_json(force=True, silent=True)
  return response_maker(info_cards.corpus(corpus))


@app.route('/summary/corpus', methods=["POST"])
def api_summary_corpus():
  corpus = request.get_json(force=True, silent=True)
  return response_maker(summary.corpus(corpus))


@app.route('/search/<string:word>')
def api_search_word(word):
  return response_maker(search_word(word))


if __name__ == "__main__":
  app.run(port=environ.get("PORT"))
