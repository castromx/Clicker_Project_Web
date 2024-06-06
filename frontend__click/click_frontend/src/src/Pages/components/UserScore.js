import React from 'react';

const UserScore = ({ scoreData }) => {
    return (
        <div className="user-score">
            <h1>User Score</h1>
            <p>Score: {scoreData.score}</p>
        </div>
    );
}

export default UserScore;
