import './App.css';
import React, { useState } from 'react';
import SearchBar from './components/SearchBar.js';
import Results from './components/Results';
function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (query) => {
      const response = await fetch(`http://localhost:5000/search?query=${query}`);
      const data = await response.json();
      setResults(data);
  };

  return (
    <div className="App">
      <h1>Rapid Finance</h1>
      <h4>Search for News</h4>
      <SearchBar onSearch={handleSearch} />
      <Results results={results} />
    </div>
  );
}

export default App;