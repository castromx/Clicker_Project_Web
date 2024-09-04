import React from 'react';

class Image extends React.Component {

    render() {
        return (
            <img className='main-photo' src={this.props.image} alt="User Icon"></img>
        );
    }
}

export default Image;
