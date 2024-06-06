import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Clan from './components/Clan';

const ClanPage = () => {
    const [clanData, setClanData] = useState(null);
    const [clanMembers, setClanMembers] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_all_clans')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });
    }, []);

    const handleClickClan = (clanId) => {
        axios.get(`http://127.0.0.1:8000/clan_members?clan_id=${clanId}`)
            .then(response => {
                setClanMembers(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan members:', error);
            });
    };

    return (
        <div className="content-container">
            {clanData && <Clan clansData={clanData} onClickClan={handleClickClan} />}
            {clanMembers && (
                <div className="clan-members">
                    <h2>Clan Members</h2>
                    <ul>
                        {clanMembers.map(member => (
                            <li key={member.id}>{member.name}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ClanPage;
