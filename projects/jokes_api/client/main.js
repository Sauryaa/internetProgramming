"use strict";

const API_URL = "http://127.0.0.1:5000/api/v1/jokes";
const NO_JOKES_MESSAGE =
  "There are no jokes in the chosen combination of languages and categories";

const selectors = {
  form: document.getElementById("jokeForm"),
  language: document.getElementById("selLang"),
  category: document.getElementById("selCat"),
  number: document.getElementById("selNum"),
  jokeId: document.getElementById("jokeId"),
  jokes: document.getElementById("jokes"),
};

selectors.form.addEventListener("submit", handleSubmit);

async function handleSubmit(event) {
  event.preventDefault();
  const idFieldValue = selectors.jokeId.value.trim();

  if (idFieldValue.length > 0) {
    const jokeId = Number(idFieldValue);
    if (!Number.isInteger(jokeId) || jokeId < 0) {
      renderError("Please enter a non-negative joke id.");
      return;
    }
    renderLoading();
    try {
      const data = await requestJSON(`${API_URL}/${jokeId}`);
      renderSingleJoke(data.joke);
    } catch (error) {
      renderError(error.message);
    }
    return;
  }

  const language = selectors.language.value;
  const category = selectors.category.value;
  const number = selectors.number.value;

  const endpoint =
    number === "all"
      ? `${API_URL}/${language}/${category}/all`
      : `${API_URL}/${language}/${category}/${number}`;

  renderLoading();
  try {
    const data = await requestJSON(endpoint);
    const jokes = normalizeJokeList(data.jokes);
    if (jokes.length === 0) {
      renderWarning(NO_JOKES_MESSAGE);
    } else {
      renderJokeList(jokes);
    }
  } catch (error) {
    renderError(error.message);
  }
}

async function requestJSON(endpoint) {
  const response = await fetch(endpoint, {
    headers: { Accept: "application/json" },
  }).catch((error) => {
    throw new Error(error.message || "Unable to reach the jokes API.");
  });

  let payload = {};
  try {
    payload = await response.json();
  } catch (error) {
    // Ignore JSON parsing errors and fall back to an empty object
  }

  if (!response.ok) {
    const message =
      typeof payload?.error === "string"
        ? payload.error
        : `Request failed with status ${response.status}`;
    throw new Error(message);
  }
  return payload;
}

function normalizeJokeList(jokes) {
  if (!Array.isArray(jokes)) {
    return [];
  }
  return jokes
    .map((joke) => {
      if (typeof joke === "string") {
        return joke;
      }
      if (joke && typeof joke === "object") {
        return joke.text ?? "";
      }
      return "";
    })
    .filter((text) => text.length > 0);
}

function renderJokeList(jokes) {
  clearJokes();
  jokes.forEach((text, index) => {
    selectors.jokes.appendChild(createJokeArticle(text, `#${index + 1}`));
  });
}

function renderSingleJoke(joke) {
  clearJokes();
  if (!joke) {
    renderWarning(NO_JOKES_MESSAGE);
    return;
  }
  const text =
    typeof joke === "string"
      ? joke
      : typeof joke.text === "string"
      ? joke.text
      : "";
  if (!text) {
    renderWarning(NO_JOKES_MESSAGE);
    return;
  }
  const label =
    joke && typeof joke === "object"
      ? `#${joke.id ?? "?"} • ${String(joke.language || "").toUpperCase()}`
      : "#1";
  selectors.jokes.appendChild(createJokeArticle(text, label));
}

function renderLoading() {
  clearJokes();
  selectors.jokes.appendChild(createMessageArticle("Fetching the best jokes...", "info"));
}

function renderWarning(message) {
  clearJokes();
  selectors.jokes.appendChild(createMessageArticle(message, "warning"));
}

function renderError(message) {
  clearJokes();
  selectors.jokes.appendChild(createMessageArticle(message, "danger"));
}

function clearJokes() {
  selectors.jokes.replaceChildren();
}

function createJokeArticle(text, label) {
  const article = document.createElement("article");
  if (label) {
    const heading = document.createElement("strong");
    heading.textContent = label;
    article.appendChild(heading);
  }
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  article.appendChild(paragraph);
  return article;
}

function createMessageArticle(text, tone) {
  const article = document.createElement("article");
  if (tone) {
    article.classList.add(`is-${tone}`);
  }
  article.textContent = text;
  return article;
}
