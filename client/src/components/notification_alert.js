export default function useNotification (message, message_type){ // message type -> info / success / warning / error
    alert(message_type + ': ' + message)
}