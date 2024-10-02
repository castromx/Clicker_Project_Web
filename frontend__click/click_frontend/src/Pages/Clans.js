import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Clan from './components/Clan';
import ClanMembersMenu from './components/ClanMembersMenu';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ClanPage = () => {
    const [clanData, setClanData] = useState(null);
    const [clanMembers, setClanMembers] = useState(null);
    const [selectedClanId, setSelectedClanId] = useState(null);
    const [userId] = useState(1);

    useEffect(() => {
        axios.get('http://localhost:8000/get_leaderboard_clan')
            .then(response => {
                setClanData(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan data:', error);
            });
    }, []);

    useEffect(() => {
        if (selectedClanId) {
            updateClanMembers(selectedClanId);
        }
    }, [selectedClanId]);

    const handleClickClan = (clanId) => {
        setSelectedClanId(clanId);
    };

    const handleCloseMenu = () => {
        setClanMembers(null);
        setSelectedClanId(null);
    };

    const handleEnterClan = () => {
        if (selectedClanId) {
            axios.post(`http://localhost:8000/enter_in_clan?user_id=${userId}&clan_id=${selectedClanId}`)
            .then(response => {
                if (response.data.message) {
                    toast.error(response.data.message);
                } else {
                    toast.success('You have successfully joined the clan');
                    updateClanMembers(selectedClanId); 
                }
            })
            .catch(error => {
                console.error('Error entering clan:', error);
                toast.error('You need to leave the previous clan to join this one');
            });
        }
    };

    const handleExitClan = () => {
        axios.delete(`http://localhost:8000/leave_from_clan?user_id=${userId}`)
        .then(response => {
            toast.success(response.data.msg);
            updateClanMembers(selectedClanId);
        })
        .catch(error => {
            console.error('Error leaving clan:', error);
            toast.error('The user was not in a clan');
        });
    };

    const updateClanMembers = (clanId) => {
        axios.get(`http://localhost:8000/clan_members?clan_id=${clanId}`)
            .then(response => {
                setClanMembers(response.data);
            })
            .catch(error => {
                console.error('Error fetching clan members:', error);
            });
    };

    return (
        <div className="content-container">
            <ToastContainer />
            {clanData && <Clan clansData={clanData} onClickClan={handleClickClan} />}
            {clanMembers && 
                <ClanMembersMenu 
                    members={clanMembers} 
                    onClose={handleCloseMenu} 
                    onEnterClan={handleEnterClan}
                    onExitClan={handleExitClan}
                    clanId={selectedClanId}
                />
            }
        </div>
    );
};

export default ClanPage;
