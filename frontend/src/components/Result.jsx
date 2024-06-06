export default function Result(props) {
    return (
      <a
        href={props.link}
        prefetch="false"
        className="bg-gray-100 rounded-lg p-4 dark:bg-gray-700 dark:text-gray-200"
      >
        <h4 className="text-lg font-medium mb-2">{props.title}</h4>
        <p className="text-gray-600 dark:text-gray-400">{props.description}</p>
        <p className="text-gray-600 dark:text-gray-400">{props.date}</p>
        <p className="text-gray-600 dark:text-gray-400">Similarity Score: {props.score}</p>
      </a>
    );
}