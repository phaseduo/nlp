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
  except (BaseException, RuntimeError) as e:
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


@app.route('/api')
def api_entrypoint():
  return json.jsonify(
    status=200,
    message="microservice:nlp",
    data=dict()
  )


@app.route('/api/cards/sentence', methods=["POST"])
def api_cards_sentence():
  sentence = request.get_json(force=True, silent=True)
  return response_maker(lambda: info_cards.sentence(sentence))


@app.route('/api/cards/corpus', methods=["POST"])
def api_cards_corpus():
  corpus = request.get_json(force=True, silent=True)
  return response_maker(lambda: info_cards.corpus(corpus))


@app.route('/api/summary/corpus', methods=["POST"])
def api_summary_corpus():
  corpus = request.get_json(force=True, silent=True)
  return response_maker(lambda: summary.corpus(corpus))


@app.route('/api/search/<string:word>')
def api_search_word(word):
  return response_maker(lambda: search_word(word))


if __name__ == "__main__":
  app.run(host="0.0.0.0",
          port=int(environ.get("PORT")))
