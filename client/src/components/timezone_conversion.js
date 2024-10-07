const DateTimeDisplay = ({ datetimeString }) => { // has to be in ISO 8601 format eg 2024-10-02 21:35:34.602129+02:00
    // convert the datetime string to a JavaScript Date object
    const date = new Date(datetimeString);
    
    // format the date to local time without seconds and microseconds
    const formattedDate = date.toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour12: false
    });

    // Return formatted date inside a <div> or any other JSX element
    return <div>{formattedDate}</div>;
}

export default DateTimeDisplay;
