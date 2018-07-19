import WebSocketBridge from "./ws_wrapper";

export class BaseSubscription {
    constructor(debug) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = "/ws/";
        this.webSocketBridge = new WebSocketBridge();
        this.connected = false;
        this.allow_send = false;
    }
    connect() {
        if (this.debug) console.debug("Connecting");
        this.webSocketBridge.connect(this.url);
        var self = this;
        this.webSocketBridge.listen(function(action, stream) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected");
        this.connected = true;
    }
    onmessage(action) {
        if (this.debug) console.debug("Message received");
        for (let listener in this.listeners) {
            this.listeners[listener](action);
        }
    }
    subscribe(callback) {
        if (!this.connected) {
            console.error(
                "Can't subscribe, websocket disconnected! Call .connect()"
            );
            return;
        }
        this.listeners.push(callback);
        if (this.debug) console.debug("Subscribed to " + this.url);
    }
    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) console.debug("Unsubscribed from " + this.url);
    }
    send(payload) {
        if (!this.allow_send) {
            console.error("This socket does not accept messages");
            return;
        }
        if (!this.connected) {
            console.error("Can't send messages to a disconnected socket");
            return;
        }
        this.webSocketBridge.send(payload);
        if (this.debug) console.debug("Payload send to " + this.url);
    }
    disconnect() {
        this.webSocketBridge.close();
        if (this.debug) console.debug("Disconnected");
        this.connected = false;
    }
}

export class ModelSubscription extends BaseSubscription {
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

export class SelfSubscription extends BaseSubscription {
    constructor(signal, debug) {
        super(debug);
        this.signal = signal;
        this.url = "/ws/subscriptions/instances/me/" + signal + "/";
    }
}

export class GenericSubscription extends BaseSubscription {
    constructor(url, debug) {
        super(debug);
        this.url = url;
        this.allow_send = true;
    }
}
