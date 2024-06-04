import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserDetails from './components/UserDetails';
import UserScore from './components/UserScore';
import Image from './components/Image';
import Clan from './components/Clan';
import image from "./img/image.png";

const UserPage = () => {
    const [userData, setUserData] = useState(null);
    const [userScore, setUserScore] = useState(null);
    const [chargeCount, setChargeCount] = useState(null);
    const [clanData, setClanData] = useState(null);

    const fetchChargeCount = () => {
        axios.get('http://localhost:8000/get_user_boosts?user_id=1')
            .then(response => {
                setChargeCount(response.data.charge_count);
            })
            .catch(error => {
                console.error('Error fetching user boosts:', error);
            });
    };

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_user?id=1')
            .then(response => {
                setUserData(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });

        axios.get('http://127.0.0.1:8000/get_user_score?user_id=1')
            .then(response => {
                setUserScore(response.data);
            })
            .catch(error => {
                console.error('Error fetching user score:', error);
            });

        axios.get('http://127.0.0.1:8000/get_user_clan?user_id=1')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });

        fetchChargeCount();
    }, []);

    const handleIconClick = () => {
        axios.post("http://localhost:8000/add_user_scores?user_id=1&count=1", {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            setUserScore(prevScore => ({
                ...prevScore,
                score: response.data.count
            }));
            fetchChargeCount();
        })
        .catch(error => {
            console.error('Error adding user score:', error);
        });
    };

    return (
        <div className="content-container">
            {userData && <UserDetails userData={userData} />}
            {userScore && <UserScore scoreData={userScore} />}
            <p>Charge count: {chargeCount}</p>
            <Image image={image} onClick={handleIconClick} />
            {clanData && <Clan clansData={clanData} />}
        </div>
    );
};

export default UserPage;
