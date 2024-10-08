const now = new Date();
const minutes = String(now.getMinutes());
  
console.log("Current Rounded Minutes:", minutes);

if (minutes === '25'){
    console.log('yes')
}else{
    console.log('no')
}