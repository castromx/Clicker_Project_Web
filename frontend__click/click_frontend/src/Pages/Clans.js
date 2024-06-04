import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Clan from './components/Clan';

const ClanPage = () => {
    const [clanData, setClanData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_all_clans')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });
    }, []);

    return (
        <div className="content-container">
            {clanData && <Clan clansData={clanData} />}
        </div>
    );
};

export default ClanPage;
