function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    try {
        var tokenParsed = JSON.parse(window.atob(base64));
        return tokenParsed;
    }
    catch(err) {
        console.log(err);
    }

}