import { Message, useToaster } from "rsuite";

export default function useNotification (message, message_type){ // message type -> info / success / warning / error
    // const toaster = useToaster();
    
    // // push notification message
    // toaster.push(<Message>{message}</Message>, {
    //     placement: 'topCenter',
    //     closable: true,
    //     type: message_type,
    //     showIcon: true,
    //     duration: 15000
    // });
    alert(message_type + ': ' + message)
}