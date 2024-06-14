import React from 'react';

const UserCard = ({ userData }) => {
    const users = Array.isArray(userData) ? userData : [userData];
    
    return (
        <>
            {users.map(user => (
                <div className="user-container">
                    <div key={user.id} className="user-info">
                        <p className="user-name">{user.name}</p>
                        <p className="user-points">Points: {user.scores?.score}</p>
                    </div>
                </div>
            ))}
        </>
    );
};

export default UserCard;
