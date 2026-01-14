function getCookie(name) {
    let value = null;
    if (document.cookie) {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                value = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return value;
}
