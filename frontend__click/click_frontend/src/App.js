import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserDetails from './components/UserDetails';
import UserScore from './components/UserScore';
import Image from './components/Image';
import image from "./img/image.png"

const UserPage = () => {
    const [userData, setUserData] = useState(null);
    const [userScore, setUserScore] = useState(null);

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
    }, []);

    return (
        <div>
            {userData && <UserDetails userData={userData} />} 
            {userScore && <UserScore scoreData={userScore} />}
            <Image image={image}/>
        </div>
    );
}

export default UserPage;
