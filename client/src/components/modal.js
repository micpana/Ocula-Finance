// Modal.js
import React from 'react';
import './modal.css'; // optional for styling

const Modal = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null; // Do not render the modal if it is not open

    // Function to handle clicks on the overlay
    const handleOverlayClick = (e) => {
        if (e.target === e.currentTarget) {
            onClose(); // Call the onClose function if the overlay is clicked
        }
    }

    return (
        <div className="modal-overlay" 
            onClick={handleOverlayClick}
        >
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
