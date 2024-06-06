import { useState, useEffect } from "react";
import { Result } from "./components";
import { Query } from "./functions";

function App() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    const results = await Query(search);
    setResults(results);
  };

  const handleSearchValueChange = (e) => {
    setSearch(e.target.value);
  };
  
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
      <h1 className="text-white font-bold text-3xl mb-4">
        Yahoo Finance Search Engine
      </h1>
      <div className="w-full max-w-3xl px-4 md:px-0">
        <div className="relative">
          <input
            type="search"
            placeholder="Search..."
            className="w-full px-4 py-3 pr-12 text-lg rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-200"
            value={search}
            onChange={handleSearchValueChange}
          />
          <button
            onClick={handleSearch}
            className="absolute top-1/2 right-4 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
          >
            <p>Search</p>
          </button>
        </div>
        {results && (
          <div className="mt-8">
            <div className="bg-white rounded-lg shadow-md p-4 dark:bg-gray-800">
              <h3 className="text-lg font-medium mb-2 dark:text-gray-200">
                Search Results
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {results.map((item, index) => {
                  return (
                    <Result
                      key={index}
                      title={item.title}
                      date={item.date}
                      description={item.description}
                      link={item.link}
                    />
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
