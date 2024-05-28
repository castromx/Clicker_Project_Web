import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserDetails from './components/UserDetails';
import UserScore from './components/UserScore';
import Image from './components/Image';
import image from "./img/image.png";

const UserPage = () => {
    // Створення станів для даних користувача, його балів і кількості заряду
    const [userData, setUserData] = useState(null);
    const [userScore, setUserScore] = useState(null);
    const [chargeCount, setChargeCount] = useState(null);

    // Функція для отримання кількості заряду користувача
    const fetchChargeCount = () => {
        axios.get('http://localhost:8000/get_user_boosts?user_id=1')
            .then(response => {
                setChargeCount(response.data.charge_count);
            })
            .catch(error => {
                console.error('Error fetching user boosts:', error);
            });
    };

    // Ефект, який запускається при першому рендері компонента
    useEffect(() => {
        // Запит до сервера для отримання даних користувача
        axios.get('http://127.0.0.1:8000/get_user?id=1')
            .then(response => {
                setUserData(response.data);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
            });

        // Запит до сервера для отримання балів користувача
        axios.get('http://127.0.0.1:8000/get_user_score?user_id=1')
            .then(response => {
                setUserScore(response.data);
            })
            .catch(error => {
                console.error('Error fetching user score:', error);
            });

        // Отримання кількості заряду користувача
        fetchChargeCount(); 

    }, []);

    // Обробник події кліку по іконці
    const handleIconClick = () => {
        axios.post("http://localhost:8000/add_user_scores?user_id=1&count=1", {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            // Оновлення балів користувача після успішного запиту
            setUserScore(prevScore => ({
                ...prevScore,
                score: response.data.count
            }));
            // Оновлення кількості заряду після успішного запиту
            fetchChargeCount();
        })
        .catch(error => {
            console.error('Error adding user score:', error);
        });
    };

    // Відображення компонентів з даними користувача, його балів і кількості заряду
    return (
        <div>
            {userData && <UserDetails userData={userData} />}
            {userScore && <UserScore scoreData={userScore} />}
            <p>Charge count: {chargeCount}</p>
            <Image image={image} onClick={handleIconClick} />
        </div>
    );
};

export default UserPage;
