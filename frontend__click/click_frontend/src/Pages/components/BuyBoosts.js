import React from 'react';
const BuyBoosts = ({ boostsData }) => {
    return (
        <div className="buy-boosts-details">
            <h1>Buy boosts</h1>
            <div className='fill-char-count-class'>
                <p>Fill Char Count: {boostsData.fill_char_count}</p>
                <p>Your lvl: {boostsData.fill_char_count}/3</p>
                <button className='boosts-button-class'>Buy {boostsData.fill_char_count * 10}</button>
            </div>
            <div className='mine-coint-class'>
                <p>Mine Point: {boostsData.mine_coint}</p>
                <p>Your lvl: {boostsData.mine_coint}/3</p>
                <button className='boosts-button-class'>Buy {boostsData.mine_coint * 10}</button>
            </div>
            <div className='charge-count-class'>
                <p>Charge Count: {boostsData.charge_count}</p>
                <p>Your lvl: {boostsData.charge_count}/3</p>
                <button className='boosts-button-class'>Buy {boostsData.charge_count * 10}</button>
            </div>
        </div>
    );
}

export default BuyBoosts;
