

var trackEvent = function(eventName, params) {
    // We'll return a promise, and resolve it when either Gtag handles
    // our event, or a maximum fallback period elapses. Promises can
    // only be resolved once, so this also ensures whatever callbacks
    // are attached to the promise only execute once.
    var dfd = $.Deferred();

    var callback = function(){
        dfd.resolve();
    };

    // Tell Gtag to resolve our promise when it's done.
    var params = $.extend(params, {
        event_callback: callback
    });

    gtag('event', eventName, params);

    // Wait a maximum of 2 seconds for Gtag to resolve promise.
    setTimeout(callback, 2000);

    return dfd.promise();
};

var trackEventMP = function(eventName, params) {
    // We'll return a promise, and resolve it when either Gtag handles
    // our event, or a maximum fallback period elapses. Promises can
    // only be resolved once, so this also ensures whatever callbacks
    // are attached to the promise only execute once.
    var dfd = $.Deferred();
  
    var callback = function(){
        dfd.resolve();
    };
  
    // Returns either an array, or undefined.
    var measurementProtocolDetails = window.dataLayer.filter(function(row){
        return row[0] === 'measurement_protocol';
    })[0];
  
    if (measurementProtocolDetails) {
        var measurementParams = {
            measurement_id: measurementProtocolDetails[1],
            api_secret: measurementProtocolDetails[2]
        }
        if (measurementProtocolDetails[3]) {
            params['debug_mode'] = '1';
        }
  
        // Set a random client_id (2 32-bit integers seperated by a dot).
        // Note this random approach means the GA debugView won't work.
        // (To get that to work, you need to turn back on the cookies,
        // then use the same client_id as in in the _ga cookie.)
        var client_id = Math.floor(Math.random() * 1000000000) + '.' + Math.floor(Math.random() * 1000000000);
        // print response to console
        $.ajax({
            url: 'https://www.google-analytics.com/mp/collect?' + $.param(measurementParams),
            method: 'POST',
            data: JSON.stringify({
                client_id: client_id,
                events: [{
                    name: eventName,
                    params: params
                }]
            })
        }).always(callback);
  
        // Wait a maximum of 2 seconds for ajax to resolve.
        setTimeout(callback, 2000);
  
    } else {
        // Measurement Protocol not available. Resolve promise immediately.
        callback();
    }
  
    return dfd.promise();
  };