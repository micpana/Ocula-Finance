const DateTimeDisplay = ({ datetimeString }) => {
    const datetimeString = '2024-10-02 21:35:34.602129+02:00';

    // Convert the datetime string to a JavaScript Date object
    const date = new Date(datetimeString);
    
    // Format the date to local time without seconds and microseconds
    const formattedDate = date.toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour12: false
    });

    // return formatted date
    return formattedDate
}