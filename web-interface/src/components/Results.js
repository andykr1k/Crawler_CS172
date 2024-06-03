import React from "react";

const Results = ({results}) => {
    return (
        <div>
        {results.map((result, index) => (
            <div key={index}>
                <h3>{result.title}</h3>
                <p>{result.body}</p>
                <p>Score: {result.score}</p>
            </div>
        ))}
    </div>
    );
}

export default Results;