function throttle(fn, delay = 300, trailing = true) {
    let lastTime = 0;
    let timer = null;

    return function (...args) {
        const now = Date.now();
        const context = this;
        const remaining = delay - (now - lastTime);

        if (remaining <= 0) {
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            lastTime = now;
            fn.apply(context, args);
        } else if (!timer && trailing) {
            timer = setTimeout(() => {
                timer = null;
                lastTime = Date.now();
                fn.apply(context, args);
            }, remaining);
        }
    };
}

function debounce(fn, delay = 300, immediate = false) {
    let timer = null;

    return function (...args) {
        const context = this;

        if (timer) {
            clearTimeout(timer);
        }

        if (immediate) {
            const callNow = !timer;
            timer = setTimeout(() => {
                timer = null;
            }, delay);
            if (callNow) {
                fn.apply(context, args);
            } else {
                timer = setTimeout(() => {
                    fn.apply(context, args);
                }, delay);
            }
        }
    };
}

function deepClone(obj, cache = new Map()) {
    if (obj === null || typeof obj !== "object") {
        return obj;
    }

    if (cache.has(obj)) {
        return cache.get(obj);
    }

    if (obj instanceof Date) {
        return new Date(obj);
    }

    if (obj instanceof RegExp) {
        return new RegExp(obj);
    }

    if (obj instanceof Map) {
        const mapCopy = new Map();
        cache.set(obj, mapCopy);
        obj.forEach((value, key) => {
            mapCopy.set(key, deepClone(value, cache));
        });
        return mapCopy;
    }

    if (obj instanceof Set) {
        const setCopy = new Set();
        cache.set(obj, setCopy);
        obj.forEach((value) => {
            setCopy.add(deepClone(value, cache));
        });
        return setCopy;
    }

    if (Array.isArray(obj)) {
        const arrCopy = [];
        cache.set(obj, arrCopy);
        for (let i = 0; i < obj.length; i++) {
            arrCopy[i] = deepClone(obj[i], cache);
        }
        return arrCopy;
    }

    const objCopy = {};
    cache.set(obj, objCopy);
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            objCopy[key] = deepClone(obj[key], cache);
        }
    }
    return objCopy;
}



const Cookie = {
    delCookie: (name) => {
    const Days = -1;
    const exp = new Date();
    const value = Cookie.getCookie(name);
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie =
     name + '=' + escape(value) + ';expires=' + exp.toUTCString();
    },
    
    setCookie: (name, value) => {
    const Days = 30;
    const exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie =
     name + '=' + escape(value) + ';expires=' + exp.toUTCString();
    },
    
    getCookie: (name) => {
    const reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)');
    const arr = document.cookie.match(reg);
    if (arr != null) return unescape(arr[2]);
    else return null;
    },
    };
