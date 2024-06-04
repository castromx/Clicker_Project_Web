import React from 'react';

const Clan = ({ clansData }) => {
    // Перетворимо одиночний об'єкт на масив для уніфікації обробки
    const clans = Array.isArray(clansData) ? clansData : [clansData];

    return (
        <>
            {clans.map(clan => (
                <div key={clan.id} className="clan-container">
                    <div className="clan-info">
                        <p className="clan-name">{clan.name}</p> <p className="clan-points">К-ть поінтів: {clan.count_score.score}</p>
                        {clan.img_id && (
                            <img
                                src={`http://localhost:8000/images/${clan.img_id}`}
                                alt={`${clan.name} logo`}
                                className="clan-image"
                            />
                        )}
                    </div>
                </div>
            ))}
        </>
    );
};

export default Clan;
