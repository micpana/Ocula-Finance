// Modal.js
import React from 'react';
import './modal.css'; // optional for styling

const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null; // Do not render the modal if it is not open

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{backgroundColor: '#ffffff'}}>
                <button className="close-button" onClick={onClose}>
                    &times;
                </button>
                <div className="modal-children">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default Modal;
