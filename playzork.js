const frotz = require('frotz-interfacer');
 
let interfacer = new frotz({
});
 
interfacer.iteration('look', (error, output) => {
    if (error) {
        console.log(error.error);
    } else {
        console.log(output.pretty);
    }
});