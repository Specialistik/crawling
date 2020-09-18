var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug'
});


casper.start("https://www.business-gazeta.ru/article/406831", function() {
    casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36');
    this.waitForSelector('form[action="/polls/vote"]');

    casper.thenEvaluate(function() {
        this.click('input[id="radio-variant-f164-148252"][value="yes"]');
        document.querySelector('input[id="radio-variant-f164-148252"]').setAttribute('selected', true);
        document.querySelector("form[action='/polls/vote']").submit();
    });

    casper.on('resource.received', function(resp) {
        this.echo(JSON.stringify(resp, null, 4));
    });

    casper.then(function () {
        console.log('clicked ok, new location is ' + this.getCurrentUrl());
    });


    
});


casper.run(function() {
    console.log('casper run has been entered');
    //console.log(this.getCurrentUrl(), this.response()); 
    this.exit();
});