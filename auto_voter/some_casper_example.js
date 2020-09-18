//DISPLAY=:0 node test2.js
var phantom = require('phantom');
console.log('Hello, world!');
phantom.create(function (ph) {
    ph.casperPath = '/opt/libs/casperjs'
    ph.injectJs('/opt/libs/casperjs/bin/bootstrap.js');
    var casper = require('casper').create();
    casper.start('http://google.fr/');

    casper.thenEvaluate(function (term) {
        document.querySelector('input[name="q"]').setAttribute('value', term);
        document.querySelector('form[name="f"]').submit();
    }, {
        term: 'CasperJS'
    });

    casper.then(function () {
        // Click on 1st result link
        this.click('h3.r a');
    });

    casper.then(function () {
        console.log('clicked ok, new location is ' + this.getCurrentUrl());
    });

    casper.run();
});