# PhaseDuo NLP
> NLP Microservice for PhaseDuo

PhaseDuo is a web application that simplifies any content for the everyday person. From news to tech blogs and articles, we present everything in an understandable format - so you don't have to do the hard work!

This microservice handles receiving a sentence or chunk of text, analyzing the key topics on that piece of text and overlaying definitions for domain-specific words that are found on that sentence/text. This microservice is used for the flash cards that are displayed alongisde the video, as well as the summary that plays out on the video.

## API Endpoints

All the API endpoints are accessible under the prefix `<hostname>/api/`. All the API outputs are of the form:

```json
{
  "status": "<int>",
  "message": "<string>",
  "data": "<ApiEndpointOutput>"
}
```

1. `/cards/sentence`
  * Given a sentence, find key topics, form "card" objects around those important key terms and define those key topics in that sentence.
    * **POST**
    * Accepts {sentence}
    * Returns [{topic, shortDescription, description, entity, imgUrl}]
2. `/cards/corpus`
  * Given a corpus of text, find key topics, form "card" objects around those important key terms and define those key topics in that corpus.
    * **POST**
    * Accepts {corpus}
    * Returns [{topic, shortDescription, description, entity, imgUrl}]
3. `/summary/corpus`
  * Summarize an entire corpus of text.
    * **POST**
    * Accepts {corpus}
    * Returns {summary}
3. `/search/<word>`
  * Search for the definition/explanation of a word
    * **GET**
    * Returns [{topic, shortDescription, description, entity, imgUrl}]

