import React from "react";

function extractSnippet(description, query, maxLength = 180) {
  const queryLower = query.toLowerCase();
  const descriptionLower = description.toLowerCase();
  const startIdx = descriptionLower.indexOf(queryLower);

  if (startIdx === -1) {
    return description.slice(0, maxLength);
  }

  const endIdx = startIdx + query.length;

  let sentenceStart = description.lastIndexOf(".", startIdx) + 1;
  if (sentenceStart === 0) {
    sentenceStart = 0;
  }

  let sentenceEnd = description.indexOf(".", endIdx);
  if (sentenceEnd === -1) {
    sentenceEnd = description.length;
  } else {
    sentenceEnd += 1;
  }

  let snippet = description.slice(sentenceStart, sentenceEnd).trim();

  if (snippet.length > maxLength) {
    snippet = snippet.slice(0, maxLength).trim() + "...";
  }

  const highlightedSnippet = snippet.replace(
    new RegExp(`(${query})`, "i"),
    '<span class="font-bold text-blue-400">$1</span>'
  );

  return highlightedSnippet;
}

export default function Result(props) {
  const highlightedDescription = extractSnippet(props.description, props.query);

  return (
    <div className="bg-gray-100 rounded-lg p-4 dark:bg-gray-700 dark:text-gray-200">
      <h4 className="text-lg font-medium">{props.title}</h4>
      <a
        href={props.link}
        prefetch="false"
        className="bg-gray-100 rounded-lg dark:bg-gray-700 dark:text-gray-200"
      >
        <p className="text-blue-400"> {props.link}</p>
      </a>
      <p className="text-gray-600 dark:text-gray-400">
        <span dangerouslySetInnerHTML={{ __html: highlightedDescription }} />
      </p>
      <p className="text-gray-600 dark:text-gray-400">
        Similarity Score: {props.score}
      </p>
    </div>
  );
}
