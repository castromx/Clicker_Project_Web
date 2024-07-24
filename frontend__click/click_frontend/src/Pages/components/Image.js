import React, { useState } from 'react';

const Image = (props) => {
    const [animate, setAnimate] = useState(false);

    const handleClick = () => {
        setAnimate(true);
        setTimeout(() => setAnimate(false), 1000);
        if (props.onClick) {
            props.onClick();
        }
    };

    return (
        <img
            src={props.image}
            alt="User Icon"
            onClick={handleClick}
            className={`main-photo ${animate ? 'animate' : ''}`}
        />
    );
};

export default Image;
