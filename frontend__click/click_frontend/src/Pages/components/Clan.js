import React from 'react';

const Clan = ({ clansData }) => {
    return (
        <div className="clan-container">
            {/* <img src={image} alt="Clan Icon" className="clan-image" /> */}
            <div className="clan-info">
                <p className="clan-name">{clansData.name}</p>
                <p className="clan-points">К-ть поінтів: {clansData.count_score}</p>
            </div>
        </div>
    );
};


export default Clan;
