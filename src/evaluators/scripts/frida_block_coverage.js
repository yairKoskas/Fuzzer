"use strict"
var debugging_enabled = true
function debug(msg)   { if(debugging_enabled){console.log("[+ ("+Process.id+")] " + msg)} }
function debugCov(msg){ if(debugging_enabled){console.log("[+ ("+Process.id+")] " + msg)} }
function warning(msg) { console.warn("[!] " + msg) }

debug("loading script...")

var stalker_attached = false;
var stalker_finished = false;

// var whitelist = ['all'];

var gc_cnt = 0;

function make_maps() {
    var maps = Process.enumerateModulesSync();
    var i = 0;
    // We need to add the module id
    maps.map(function(o) { o.id = i++; });
    // .. and the module end point
    maps.map(function(o) { o.end = o.base.add(o.size); });

    return maps;
}
var maps = make_maps()

// We want to use frida's ModuleMap to create DRcov events, however frida's
//  Module object doesn't have the 'id' we added above. To get around this,
//  we'll create a mapping from path -> id, and have the ModuleMap look up the
//  path. While the ModuleMap does contain the base address, if we cache it
//  here, we can simply look up the path rather than the entire Module object.
var module_ids = {};
maps.map(function (e) {
    module_ids[e.path] = {id: e.id, start: e.base};
});

var filtered_maps = new ModuleMap(function (m) {
    if (whitelist.indexOf('all') >= 0) { return true; }

    return whitelist.indexOf(m.name) >= 0;
});

// Always trust code. #Make it faster
Stalker.trustThreshold = 0;
var stalker_events = []

var target_function = undefined

rpc.exports = {
    // get the module maps:
    makemaps: function(args) {
        return maps;
    },

    // get the PID:
    getpid: function(args) {
        return Process.id;
    },

    // get the absolute address of a function by name
    resolvesymbol: function(symbolname) {
        return DebugSymbol.fromName(symbolname).address;
    },

    // initialize the address of the target function (to-be-hooked)
    // and attach the Interceptor
    attachstalker: function() {
        stalker_attached = true
        stalker_finished = false
        Stalker.queueCapacity = 100000000
        Stalker.queueDrainInterval = 1000*1000

        debugCov("follow")
        Stalker.follow(Process.getCurrentThreadId(), {
            events: {
				compile: true
            },
            onReceive: function (events) {
                debugCov("onReceive: len(stalker_events)=" + stalker_events.length)
                stalker_events.push(events)
            }
        });
    },
    settarget: function(target) {
        target_function = ptr(target)

        Interceptor.attach(target_function, {
            onEnter: function (args) {
                debug('Called ------func-------: ');
                debug("Stalker.queueCapacity=" + Stalker.queueCapacity)
                debug("Stalker.queueDrainInterval=" + Stalker.queueDrainInterval)
				debug('Function: ' + target_function)
                stalker_attached = true
                stalker_finished = false
                Stalker.queueCapacity = 100000000
                Stalker.queueDrainInterval = 1000*1000

                debugCov("follow")
                Stalker.follow(Process.getCurrentThreadId(), {
                    events: {
						compile: true
                    },
                    onReceive: function (events) {
                        debugCov("onReceive: len(stalker_events)=" + stalker_events.length)
                        stalker_events.push(events)
                    }
                    /*onCallSummary: function (summary) {
                        console.log("onCallSummary: " + JSON.stringify(summary))
                    }*/
                });
            },
            onLeave: function (retval) {
                //debug('Leave func ');
                debugCov("unfollow")
                Stalker.unfollow(Process.getCurrentThreadId())
                debugCov("flush")
                Stalker.flush();
                if(gc_cnt % 100 == 0){
                    Stalker.garbageCollect();
                }
                gc_cnt++;
                stalker_finished = true
                //send("finished")
            }
        });
    },
    checkstalker: function(args) {
        debugCov("checkstalker: len(stalker_events)=" + stalker_events.length + 
                    "  stalker_{attached,finished}=" + stalker_attached + "," + stalker_finished)
        return [stalker_attached, stalker_finished];
    },
    // get the coverage
    getcoverage: function(args) {
        debugCov("getcoverage: len(stalker_events)=" + stalker_events.length)
        if(stalker_events.length == 0)
            return undefined;
        var accumulated_events = []
        for(var i = 0; i < stalker_events.length; i++) {
            var parsed = Stalker.parse(stalker_events[i], {stringify: false, annotate: false})
            accumulated_events = accumulated_events.concat(parsed);
        }
        return accumulated_events;
    },
    // clear the coverage (set empty)
    clearcoverage: function(args) {
        debugCov("clearcoverage")
        stalker_events = []
        stalker_attached = false
        stalker_finished = false
    }
};
debug("Loading JS complete")
