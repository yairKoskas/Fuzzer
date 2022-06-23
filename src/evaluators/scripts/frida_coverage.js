"use strict";
var whitelist = ['all'];
var threadlist = ['all'];

function make_maps() {
    var maps = Process.enumerateModulesSync();
    var i = 0;
    maps.map(function(o) { o.id = i++; });
    // .. and the module end point
    maps.map(function(o) { o.end = o.base.add(o.size); });
    return maps;
}

var maps = make_maps()
send({'map': maps});
var module_ids = {};
maps.map(function (e) {
    module_ids[e.path] = {id: e.id, start: e.base};
});
var filtered_maps = new ModuleMap(function (m) {
    if (whitelist.indexOf('all') >= 0) { return true; }
    return whitelist.indexOf(m.name) >= 0;
});
function drcov_bbs(bbs, fmaps, path_ids) {
    /*
        typedef struct _bb_entry_t {
            uint   start;      
            ushort size;
            ushort mod_id;
        } bb_entry_t;
    */
    var entry_sz = 8;
    var bb = new ArrayBuffer(entry_sz * bbs.length);
    var num_entries = 0;
    for (var i = 0; i < bbs.length; ++i) {
        var e = bbs[i];
        var start = e[0];
        var end   = e[1];
        var path = fmaps.findPath(start);
        if (path == null) { continue; }
        var mod_info = path_ids[path];
        var offset = start.sub(mod_info.start).toInt32();
        var size = end.sub(start).toInt32();
        var mod_id = mod_info.id;
        var x =  new Uint32Array(bb, num_entries * entry_sz, 1);
        x[0] = offset;
        var y = new Uint16Array(bb, num_entries * entry_sz + 4, 2);
        y[0] = size;
        y[1] = mod_id;
        ++num_entries;
    }
    return new Uint8Array(bb, 0, num_entries * entry_sz);
}

Stalker.trustThreshold = 0;

Process.enumerateThreads({
    onMatch: function (thread) {
        if (threadlist.indexOf(thread.id) < 0 &&
            threadlist.indexOf('all') < 0) {
            // This is not the thread you're look for
            return;
        }
        Stalker.follow(thread.id, {
            events: {
                compile: true
            },
            onReceive: function (event) {
                var bb_events = Stalker.parse(event,
                    {stringify: false, annotate: false});
                var bbs = drcov_bbs(bb_events, filtered_maps, module_ids);
                send({bbs: 1}, bbs);
            }
        });
    },
    onComplete: function () {}
});