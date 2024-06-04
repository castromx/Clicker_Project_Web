import React from 'react';

class Image extends React.Component {
    render() {
        return (
            <img src={this.props.image} alt="User Icon" onClick={this.props.onClick} className="main-photo" />
        );
    }
}

export default Image;
