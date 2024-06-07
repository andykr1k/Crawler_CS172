import { useState } from "react";
import { Result } from "./components";
import { Query } from "./functions";
import { MagnifyingGlass } from "react-loader-spinner";

let popular = [
  {
    query: "Stock Market News",
  },
  {
    query: "Latest Trends",
  },
  {
    query: "Nvidia",
  },
  {
    query: "Apple",
  },
  {
    query: "Google",
  },
  {
    query: "OpenAI",
  },
  {
    query: "Tesla",
  },
  {
    query: "Microsoft",
  },
];

function App() {
  const [search, setSearch] = useState("");
  const [lastsearch, setLastsearch] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const results = await Query(search);
    setLastsearch(search);
    setResults(results);
    setLoading(false);
  };

  const handleSearchValueChange = (e) => {
    setSearch(e.target.value);
  };

  const handlePopularSearchClick = async (query) => {
    setLoading(true);
    setSearch(query);
    const results = await Query(query);
    setLastsearch(search);
    setResults(results);
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 min-h-screen">
      <h1 className="text-white font-bold text-5xl mb-20 mt-20">
        Yahoo Finance Search Engine
      </h1>
      <div className="w-full max-w-5xl px-4 md:px-0">
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
        {loading ? (
          <div className="flex justify-center mt-8">
            <MagnifyingGlass
              visible={true}
              height="80"
              width="80"
              ariaLabel="magnifying-glass-loading"
              wrapperStyle={{}}
              wrapperClass="magnifying-glass-wrapper"
              glassColor="#c0efff"
              color="#e15b64"
            />
          </div>
        ) : (
          <>
            {results ? (
              <div className="mt-8  mb-20">
                <div className="bg-white rounded-lg shadow-md p-4 dark:bg-gray-800">
                  <h3 className="text-lg font-medium mb-2 dark:text-gray-200">
                    Search Results - {results.length} results
                  </h3>
                  <div className="grid grid-cols-1 gap-4">
                    {results.map((item, index) => {
                      return (
                        <Result
                          key={index}
                          title={item.title}
                          date={item.date}
                          description={item.text}
                          link={item.link}
                          score={item.score}
                          query={lastsearch}
                        />
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="w-full px-4 py-3 text-lg rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-gray-200 mt-8">
                <h2>Popular Searches</h2>
                <div className="grid grid-cols-4 gap-2 mt-4">
                  {popular.map((item, index) => {
                    return (
                      <button
                        key={index}
                        onClick={() => handlePopularSearchClick(item.query)}
                        className="w-full bg-gray-200 dark:bg-gray-700 p-2 rounded-lg text-center"
                      >
                        <h3 className="text-md">{item.query}</h3>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
