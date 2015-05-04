/**
 * Created by ujuc on 2015. 5. 4..
 */

var initialize = function (navigator) {
    $('#id_login').on('click', function () {
        navigator.id.request();
    });

    navigator.id.watch();
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
