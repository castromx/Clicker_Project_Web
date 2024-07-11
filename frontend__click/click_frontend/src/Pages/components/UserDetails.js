import React from 'react';

const UserDetails = ({ userData }) => {
    return (
        <div className="user-details">
            <h1>User Details</h1>
            <p>Name: {userData.name}</p>
            <p>Scores: {userData.scores.score}</p>
            <p>Chagres: {userData.charges.charge}</p>
            
        </div>
    );
}

export default UserDetails;
