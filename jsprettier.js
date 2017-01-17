'use strict';

var prettier = require("prettier");

var source = '';

process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(data) {
    source += data;
});

process.stdin.on('end', function() {
    var prettierOptions = process.argv[2],
        cwd = process.argv[3];

    var formatOptions;
    try {
        formatOptions = JSON.parse(prettierOptions);
    } catch (e) {
        formatOptions = {};
    }

    var transformed = prettier.format(source, formatOptions);
    process.chdir(cwd);
    process.stdout.write(transformed);
});
