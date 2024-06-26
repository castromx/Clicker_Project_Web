import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserCard from './components/UserCard';
import Clan from './components/Clan';

const LeaderBoardPage = () => {
    const [userData, setUserData] = useState(null);
    const [clanData, setClanData] = useState(null);
    const [selectedTab, setSelectedTab] = useState('users'); // 'users' за замовчуванням

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

    const handleTabClick = (tab) => {
        setSelectedTab(tab);
    };

    return (
        <div className="content-container">
            <div className='button-container'>
                <div className="tab-buttons">
                    <button onClick={() => handleTabClick('users')} className={selectedTab === 'users' ? 'active' : ''}>
                        Користувачі
                    </button>
                    <span className="divider">|</span>
                    <button onClick={() => handleTabClick('clans')} className={selectedTab === 'clans' ? 'active' : ''}>
                        Клани
                    </button>
                </div>
            </div>
                {selectedTab === 'users' && userData && <UserCard userData={userData} />}
                {selectedTab === 'clans' && clanData && <Clan clansData={clanData} />}
        </div>
    );
};

export default LeaderBoardPage;
