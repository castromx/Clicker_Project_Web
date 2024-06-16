import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserBoostsDetails from './components/BoostsDetail';
import BuyBoosts from './components/BuyBoosts';

const BoostsPage = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_user_boosts', {
            params: { user_id: 1 }
        })
        .then(response => {
            setUserData(response.data);
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
        });
    }, []);

    return (
        <div>
            {userData && <UserBoostsDetails userData={userData} />}
            {userData && <BuyBoosts boostsData={userData} />}
        </div>
    );
};

export default BoostsPage;
