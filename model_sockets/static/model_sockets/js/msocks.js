!(function(e, t) {
    "function" == typeof define && define.amd
        ? define([], t)
        : "undefined" != typeof module && module.exports
            ? (module.exports = t())
            : (e.ReconnectingWebSocket = t());
})(this, function() {
    function e(t, n, o) {
        function c(e, t) {
            var n = document.createEvent("CustomEvent");
            return n.initCustomEvent(e, !1, !1, t), n;
        }
        var i = {
            debug: !1,
            automaticOpen: !0,
            reconnectInterval: 1e3,
            maxReconnectInterval: 3e4,
            reconnectDecay: 1.5,
            timeoutInterval: 2e3,
            maxReconnectAttempts: null,
            binaryType: "blob"
        };
        o || (o = {});
        for (var s in i) void 0 !== o[s] ? (this[s] = o[s]) : (this[s] = i[s]);
        (this.url = t),
            (this.reconnectAttempts = 0),
            (this.readyState = WebSocket.CONNECTING),
            (this.protocol = null);
        var r,
            u = this,
            d = !1,
            l = !1,
            a = document.createElement("div");
        a.addEventListener("open", function(e) {
            u.onopen(e);
        }),
            a.addEventListener("close", function(e) {
                u.onclose(e);
            }),
            a.addEventListener("connecting", function(e) {
                u.onconnecting(e);
            }),
            a.addEventListener("message", function(e) {
                u.onmessage(e);
            }),
            a.addEventListener("error", function(e) {
                u.onerror(e);
            }),
            (this.addEventListener = a.addEventListener.bind(a)),
            (this.removeEventListener = a.removeEventListener.bind(a)),
            (this.dispatchEvent = a.dispatchEvent.bind(a)),
            (this.open = function(t) {
                if (
                    ((r = new WebSocket(u.url, n || [])),
                    (r.binaryType = this.binaryType),
                    t)
                ) {
                    if (
                        this.maxReconnectAttempts &&
                        this.reconnectAttempts > this.maxReconnectAttempts
                    )
                        return;
                } else
                    a.dispatchEvent(c("connecting")),
                        (this.reconnectAttempts = 0);
                (u.debug || e.debugAll) &&
                    console.debug(
                        "ReconnectingWebSocket",
                        "attempt-connect",
                        u.url
                    );
                var o = r,
                    i = setTimeout(function() {
                        (u.debug || e.debugAll) &&
                            console.debug(
                                "ReconnectingWebSocket",
                                "connection-timeout",
                                u.url
                            ),
                            (l = !0),
                            o.close(),
                            (l = !1);
                    }, u.timeoutInterval);
                (r.onopen = function(n) {
                    clearTimeout(i),
                        (u.debug || e.debugAll) &&
                            console.debug(
                                "ReconnectingWebSocket",
                                "onopen",
                                u.url
                            ),
                        (u.protocol = r.protocol),
                        (u.readyState = WebSocket.OPEN),
                        (u.reconnectAttempts = 0);
                    var o = c("open");
                    (o.isReconnect = t), (t = !1), a.dispatchEvent(o);
                }),
                    (r.onclose = function(n) {
                        if ((clearTimeout(i), (r = null), d))
                            (u.readyState = WebSocket.CLOSED),
                                a.dispatchEvent(c("close"));
                        else {
                            u.readyState = WebSocket.CONNECTING;
                            var o = c("connecting");
                            (o.code = n.code),
                                (o.reason = n.reason),
                                (o.wasClean = n.wasClean),
                                a.dispatchEvent(o),
                                t ||
                                    l ||
                                    ((u.debug || e.debugAll) &&
                                        console.debug(
                                            "ReconnectingWebSocket",
                                            "onclose",
                                            u.url
                                        ),
                                    a.dispatchEvent(c("close")));
                            var i =
                                u.reconnectInterval *
                                Math.pow(u.reconnectDecay, u.reconnectAttempts);
                            setTimeout(function() {
                                u.reconnectAttempts++, u.open(!0);
                            }, i > u.maxReconnectInterval
                                ? u.maxReconnectInterval
                                : i);
                        }
                    }),
                    (r.onmessage = function(t) {
                        (u.debug || e.debugAll) &&
                            console.debug(
                                "ReconnectingWebSocket",
                                "onmessage",
                                u.url,
                                t.data
                            );
                        var n = c("message");
                        (n.data = t.data), a.dispatchEvent(n);
                    }),
                    (r.onerror = function(t) {
                        (u.debug || e.debugAll) &&
                            console.debug(
                                "ReconnectingWebSocket",
                                "onerror",
                                u.url,
                                t
                            ),
                            a.dispatchEvent(c("error"));
                    });
            }),
            1 == this.automaticOpen && this.open(!1),
            (this.send = function(t) {
                if (r)
                    return (
                        (u.debug || e.debugAll) &&
                            console.debug(
                                "ReconnectingWebSocket",
                                "send",
                                u.url,
                                t
                            ),
                        r.send(t)
                    );
                throw "INVALID_STATE_ERR : Pausing to reconnect websocket";
            }),
            (this.close = function(e, t) {
                void 0 === e && (e = 1e3), (d = !0), r && r.close(e, t);
            }),
            (this.refresh = function() {
                r && r.close();
            });
    }
    if ("WebSocket" in window)
        return (
            (e.prototype.onopen = function(e) {}),
            (e.prototype.onclose = function(e) {}),
            (e.prototype.onconnecting = function(e) {}),
            (e.prototype.onmessage = function(e) {}),
            (e.prototype.onerror = function(e) {}),
            (e.debugAll = !1),
            (e.CONNECTING = WebSocket.CONNECTING),
            (e.OPEN = WebSocket.OPEN),
            (e.CLOSING = WebSocket.CLOSING),
            (e.CLOSED = WebSocket.CLOSED),
            e
        );
});
class WebSocketBridge {
    constructor(e) {
        (this.socket = null),
            (this.streams = {}),
            (this.default_cb = null),
            (this.options = {
                options: e
            });
    }
    connect(e, t, n) {
        let o;
        const c = `${"https:" === window.location.protocol ? "wss" : "ws"}://${
            window.location.host
        }`;
        (o = void 0 === e ? c : "/" == e[0] ? `${c}${e}` : e),
            (this.socket = new ReconnectingWebSocket(o, t, n));
    }
    close(e, t) {
        this.socket.close(e, t);
    }
    listen(e) {
        (this.default_cb = e),
            (this.socket.onmessage = e => {
                const t = JSON.parse(e.data);
                let n;
                let o;
                if (void 0 !== t.stream) {
                    (n = t.payload), (o = t.stream);
                    const e = this.streams[o];
                    return e ? e(n, o) : null;
                }
                return (
                    (n = t),
                    (o = null),
                    this.default_cb ? this.default_cb(n, o) : null
                );
            });
    }
    demultiplex(e, t) {
        this.streams[e] = t;
    }
    send(e) {
        this.socket.send(JSON.stringify(e));
    }
    stream(e) {
        return {
            send: t => {
                const n = {
                    stream: e,
                    payload: t
                };
                this.socket.send(JSON.stringify(n));
            }
        };
    }
}

class BaseSubscription {
    constructor(debug) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = "/ws/";
        this.webSocketBridge = new WebSocketBridge();
    }
    connect() {
        if (this.debug) console.debug("Connecting");
        this.webSocketBridge.connect(this.url);
        var self = this;
        this.webSocketBridge.listen(function(action, stream) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected");
    }
    onmessage(action) {
        if (this.debug) console.debug("Message received");
        for (listener in this.listeners) {
            listener(action);
        }
    }
    subscribe(callback) {
        this.listeners.push(callback);
        if (this.debug) console.debug("Subscribed to " + this.url);
    }
    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) console.debug("Unsubscribed from " + this.url);
    }
    disconnect() {
        this.webSocketBridge.close();
        if (this.debug) console.debug("Disconnected");
    }
}

class ModelSubscription extends BaseSubscription {
    constructor(app, model, signal, debug) {
        super(debug);
        this.model = model;
        this.signal = signal;
        this.url =
            "/ws/subscriptions/models/" +
            app +
            "/" +
            model +
            "/" +
            signal +
            "/";
    }
}

class SelfSubscription extends BaseSubscription {
    constructor(signal, debug) {
        super(debug);
        this.signal = signal;
        this.url = "/ws/subscriptions/instances/me/" + signal + "/";
    }
}

class GenericSubscription extends BaseSubscription {
    constructor(url, debug) {
        super(debug);
        this.url = url;
    }
}
