import { ToastContainer, toast } from 'react-toastify';

export default function useNotification (message, message_type){ // message type -> info / success / warning / error / default
    // alert
    toast(message, {
        position: "top-center",
        type: message_type,
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
    });
}