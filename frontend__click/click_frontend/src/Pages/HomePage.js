import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserDetails from './components/UserDetails';
import Image from './components/Image';
import Clan from './components/Clan';
import image from "./img/image.png";

const UserPage = () => {
    const [userData, setUserData] = useState(null);
    const [clanData, setClanData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_user?id_user=1')
            .then(response => {
                setUserData(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });

        axios.get('http://127.0.0.1:8000/get_user_clan?user_id=1')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });
    }, []);

    const handleIconClick = () => {
        axios.post("http://localhost:8000/add_user_scores?user_id=1&count=1", {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(() => {
            axios.get('http://127.0.0.1:8000/get_user?id_user=1')
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
