import React, { useState } from 'react';

const Image = ({ image, onClick }) => {
    const [isAnimating, setIsAnimating] = useState(false);
    const [showPlusOne, setShowPlusOne] = useState(false);

    const handleClick = () => {
        setIsAnimating(true);
        setShowPlusOne(true); 
        onClick();
    };

    const handleAnimationEnd = () => {
        setIsAnimating(false);
        setTimeout(() => {
            setShowPlusOne(false); // Сховати +1 через певний час
        }, 1000); // Тривалість показу тексту +1
    };

    return (
        <div className="image-container" style={{ position: 'relative' }}>
            <img
                className={`main-photo ${isAnimating ? 'animate' : ''}`}
                src={image}
                alt="User Icon"
                onClick={handleClick}
                onAnimationEnd={handleAnimationEnd}
            />
            {showPlusOne && (
                <span className="plus-one" style={plusOneStyle}>
                    +1
                </span>
            )}
        </div>
    );
};

const plusOneStyle = {
    position: 'absolute',
    top: '10px',
    left: '10px',
    fontSize: '24px',
    color: 'red',
    fontWeight: 'bold',
    animation: 'fade-out 1s forwards',
};

export default Image;
