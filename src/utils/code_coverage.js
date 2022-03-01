"use strict";
var whitelist = %s;
var threadlist = %s;
// Get the module map
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
send({'map': maps});
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
// This function takes a list of GumCompileEvents and converts it into a DRcov
//  entry. Note that we'll get duplicated events when two traced threads
//  execute the same code, but this will be handled by the python side.
function drcov_bbs(bbs, fmaps, path_ids) {
    // We're going to use send(..., data) so we need an array buffer to send
    //  our results back with. Let's go ahead and alloc the max possible
    //  reply size
    /*
        // Data structure for the coverage info itself
        typedef struct _bb_entry_t {
            uint   start;      // offset of bb start from the image base
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
        // We're going to create two memory views into the array we alloc'd at
        //  the start.
        // we want one u32 after all the other entries we've created
        var x =  new Uint32Array(bb, num_entries * entry_sz, 1);
        x[0] = offset;
        // we want two u16's offset after the 4 byte u32 above
        var y = new Uint16Array(bb, num_entries * entry_sz + 4, 2);
        y[0] = size;
        y[1] = mod_id;
        ++num_entries;
    }
    // We can save some space here, rather than sending the entire array back,
    //  we can create a new view into the already allocated memory, and just
    //  send back that linear chunk.
    return new Uint8Array(bb, 0, num_entries * entry_sz);
}
// Punt on self modifying code -- should improve speed and lighthouse will
//  barf on it anyways
Stalker.trustThreshold = 0;
console.log('Starting to stalk threads...');
// Note, we will miss any bbs hit by threads that are created after we've
//  attached
Process.enumerateThreads({
    onMatch: function (thread) {
        if (threadlist.indexOf(thread.id) < 0 &&
            threadlist.indexOf('all') < 0) {
            // This is not the thread you're look for
            return;
        }
        console.log('Stalking thread ' + thread.id + '.');
        Stalker.follow(thread.id, {
            events: {
                compile: true
            },
            onReceive: function (event) {
                var bb_events = Stalker.parse(event,
                    {stringify: false, annotate: false});
                var bbs = drcov_bbs(bb_events, filtered_maps, module_ids);
                // We're going to send a dummy message, the actual bb is in the
                //  data field. We're sending a dict to keep it consistent with
                //  the map. We're also creating the drcov event in javascript,
                // so on the py recv side we can just blindly add it to a set.
                send({bbs: 1}, bbs);
            }
        });
    },
    onComplete: function () { console.log('Done stalking threads.'); }
});
