var prettier = require("prettier");
var source = '';

process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function(data) {
    source += data;
});

process.stdin.on('end', function() {
    var config = process.argv[2],
        cwd = process.argv[3];

    var formatOptions;
    try {
        formatOptions = JSON.parse(config);
    } catch (e) {
        formatOptions = {};
    }

    process.chdir(cwd);
    var transformed = prettier.format(source, formatOptions);
    process.stdout.write(transformed);
});
