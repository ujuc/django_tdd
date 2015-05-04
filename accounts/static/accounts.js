/**
 * Created by ujuc on 2015. 5. 4..
 */

var initialize = function (navigator, user, token, urls) {
    $('#id_login').on('click', function () {
        navigator.id.request();
    });

    navigator.id.watch({
        loggedInUser: use,
        onlogin: function (assertion) {
        	$.post(
        		urls.login,
        		{ assertion: assertion, scrfmiddlewaretoken: token }
        	);
        	deferred.done(function () { window.location.reload(); })
        	deferred.fail(function () { navigator.id.logout(); });
        },
        onlogout: function () {}
    });
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
