var prettier = require("prettier");
var source = '';

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(data) {
    source += data;
});

process.stdin.on('end', function() {
    var formatOptions;
    try {
        formatOptions = JSON.parse(process.argv[2]);
    } catch (e) {
        formatOptions = {};
    }

    process.chdir(process.argv[3]);

    var transformed = prettier.format(source, formatOptions);
    process.stdout.write(transformed);
});
