import React from 'react';

const ClanMembersMenu = ({ members, onClose }) => {
    return (
        <div className="clan-members-menu">
            <button className="close-button" onClick={onClose}>Close</button>
            <h2>Clan Members</h2>
            <ul>
                {members.map(member => (
                    <li key={member.id}>{member.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default ClanMembersMenu;
