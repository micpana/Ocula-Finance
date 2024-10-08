const objects = [
    { attribute1: 'obj1attr1', attribute2: 'obj1attr2' },
    { attribute1: 'obj2attr1', attribute2: 'obj2attr2' },
    // Add more objects as needed
];

let text = objects.map(obj => `${obj.attribute1} ${obj.attribute2}`).join(', ');

console.log(text); // Output: "obj1attr1 obj1attr2, obj2attr1 obj2attr2"
