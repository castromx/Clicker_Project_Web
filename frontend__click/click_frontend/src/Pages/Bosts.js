import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserachivmDetails from './components/Achivments';
import BuyBoosts from './components/BuyBoosts';

const BoostsPage = () => {
    const [userData, setUserData] = useState(null);
    const [AchivmData, setAchivmData] = useState(null);

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
        axios.get('http://127.0.0.1:8000/get_user_achivments?user_id=1')
            .then(response => {
                setAchivmData(response.data);
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
    }, []);

    return (
        <div>
            {userData && <BuyBoosts boostsData={userData} />}
            {AchivmData && <UserachivmDetails achvmData={AchivmData} />}
        </div>
    );
};

export default BoostsPage;
