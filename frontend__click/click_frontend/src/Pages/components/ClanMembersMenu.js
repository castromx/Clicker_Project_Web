import React from 'react';

const ClanMembersMenu = ({ members, onClose, onEnterClan, onExitClan, clanId }) => {
    return (
        <div className="clan-members-menu">
            <button className="close-button" onClick={onClose}>Close</button>
            <h2>Clan Members</h2>
            <ul>
                {members.map(member => (
                    <li key={member.id}>
                        {member.name} - {member.scores ? member.scores.score : 'N/A'}
                    </li>
                ))}
            </ul>
            <button className='EnterClan' onClick={() => onEnterClan(clanId)}>Enter in clan</button>
            <button className='ExitClan' onClick={onExitClan}>Exit from clan</button>
        </div>
    );
};

export default ClanMembersMenu;
