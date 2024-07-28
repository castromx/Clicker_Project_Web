import React from 'react';

const UserachivmDetails = ({ achvmData }) => {

    return (
        <div className="user-achivm-details">
            <h1>User Achievements</h1>
            <p>Charge Count up to 50k: {achvmData.up_50k ? 'Achieved' : 'Not achieved'}</p>
            <p>Charge Count up to 500k: {achvmData.up_500k ? 'Achieved' : 'Not achieved'}</p>
            <p>Fill Char Count up to 100k: {achvmData.up_100k ? 'Achieved' : 'Not achieved'}</p>
            <p>Charge Count up to 1 million: {achvmData.up_1million ? 'Achieved' : 'Not achieved'}</p>
        </div>
    );
}

export default UserachivmDetails;
