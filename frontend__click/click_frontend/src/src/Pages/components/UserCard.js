import React from 'react';
import { FxemojiHampster } from '../Icons/icons';
const UserCard = ({ userData }) => {
    const users = Array.isArray(userData) ? userData : [userData];
    
    return (
        <>
            {users.map(user => (
                <div className="user-container">
                    <FxemojiHampster/>
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
