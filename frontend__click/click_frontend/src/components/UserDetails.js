import React from 'react';

const UserDetails = ({ userData }) => {
    return (
        <div className="user-details">
            <h1>User Details</h1>
            <p>Name: {userData.name}</p>
        </div>
    );
}

export default UserDetails;
