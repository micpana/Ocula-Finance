function getRoundedMinutes() {
    const now = new Date();
    const minutes = String(now.getMinutes());
    
    return String(minutes)
}
  
console.log("Current Rounded Minutes:", getRoundedMinutes());