import React from 'react';

const UserBoostsDetails = ({ userData }) => {
    return (
        <div className="user-boosts-details">
            <h1>User Boosts</h1>
            <p>Fill Char Count: {userData.fill_char_count}</p>
            <p>Mine Point: {userData.mine_coint}</p>
            <p>Charge Count: {userData.charge_count}</p>
        </div>
    );
}

export default UserBoostsDetails;
