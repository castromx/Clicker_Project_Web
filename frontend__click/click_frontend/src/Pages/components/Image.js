import React, { useState } from 'react';

const Image = ({ image, onClick }) => {
    const [isAnimating, setIsAnimating] = useState(false);

    const handleClick = () => {
        setIsAnimating(true);
        onClick();
    };

    const handleAnimationEnd = () => {
        setIsAnimating(false);
    };

    return (
        <img
            className={`main-photo ${isAnimating ? 'animate' : ''}`}
            src={image}
            alt="User Icon"
            onClick={handleClick}
            onAnimationEnd={handleAnimationEnd}
        />
    );
};

export default Image;
