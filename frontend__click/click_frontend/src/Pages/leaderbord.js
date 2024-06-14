import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserCard from './components/UserCard';
import Clan from './components/Clan';

const LeaderBoardPage = () => {
    const [userData, setUserData] = useState(null);
    const [clanData, setClanData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_leaderboard_user')
            .then(response => {
                setUserData(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });
        axios.get('http://127.0.0.1:8000/get_leaderboard_clan')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });
    }, []);


    return (
        <div className="content-container">
            {userData && <UserCard userData={userData} />}
            {clanData && <Clan clansData={clanData} />}
        </div>
    );
};

export default LeaderBoardPage;
