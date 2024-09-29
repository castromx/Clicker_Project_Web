import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserDetails from './components/UserDetails';
import Image from './components/Image';
import Clan from './components/Clan';
import image from "./img/image.png";

const UserPage = () => {
    const [userData, setUserData] = useState(null);
    const [clanData, setClanData] = useState(null);
    const [telegramUser, setTelegramUser] = useState(null);
    const [userId, setUserId] = useState(null); 

    useEffect(() => {
        const tg = window.Telegram.WebApp;
        tg.ready();
    
        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            const userId = tg.initDataUnsafe.user.id;
            setTelegramUser(tg.initDataUnsafe.user);
            setUserId(userId); 

            axios.get(`LINK/get_user?id_user=${userId}`)
                .then(response => {
                    setUserData(response.data);
                })
                .catch(error => {
                    console.error('Error fetching user data:', error);
                });

            axios.get(`LINK/get_user_clan?user_id=${userId}`)
                .then(response => {
                    setClanData(response.data);
                })
                .catch(error => {
                    console.error('Error fetching clan data:', error);
                });
        }
    }, []);

    const handleIconClick = () => {
        axios.post(`LINK/add_user_scores?user_id=${telegramUser.id}&count=1`, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(() => {
            axios.get(`LINK/get_user?id_user=${telegramUser.id}`)
                .then(response => {
                    setUserData(response.data);
                })
                .catch(error => {
                    console.error('Error fetching updated user data:', error);
                });
        })
        .catch(error => {
            console.error('Error adding user scores:', error);
        });
    };

    return (
        <div className="content-container">
            {userData && <UserDetails userData={userData} />}
            <Image image={image} onClick={handleIconClick} />
            {clanData && <Clan clansData={clanData} />}
        </div>
    );
};

export default UserPage;
