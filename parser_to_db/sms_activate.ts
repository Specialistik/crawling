//const axios = require('axios').default;

var axios = require('axios');

axios.get('https://sms-activate.ru/stubs/handler_api.php', {
    params : {
        'api_key': 'e1bfd58294A07360305082d40A929d1d',
        'action': 'getNumber',
        'service': 'ya',
        'forward': 0,
        'operator': 'any',
        'country': 0
    }
}).then(function (response) {
    console.log(response);
})
.catch(function (error) {
    console.log(error);
});

/*
    url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=e1bfd58294A07360305082d40A929d1d&action=getNumber&service=ya&forward=0&operator=any&country=0'
    r = requests.get(url)
    print('sms activate response is ' + r.text)
    spl = r.text.split(':')
    id_act, num = spl[1], spl[2]
    return id_act, num
*/