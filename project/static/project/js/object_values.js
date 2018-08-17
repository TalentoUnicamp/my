/* Polyfill service v3.25.1
 * For detailed credits and licence information see https://github.com/financial-times/polyfill-service.
 *
 * UA detected: ios_saf/10.0.0
 * Features requested: Object.values
 *
 * - Object.values, License: CC0 */

(function(undefined) {

// Object.values
(function () {
    Object.defineProperty(Object, 'values', {
        configurable: true,
        enumerable: false,
        value: function (object) {
            return Object.keys(object).map(function (key) {
                return object[key];
            });
        },
        writable: true
    });
}());
})
.call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
