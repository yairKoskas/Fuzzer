from __future__ import print_function

import argparse
import json
import pprint
import signal
import sys

import frida

with open('code_coverage.js', 'r') as f:
    SCRIPT = f.read()

modules = []
bbs = set([])


def populate_modules(image_list):
    global modules

    for image in image_list:
        idx = image['id']
        path = image['path']
        base = int(image['base'], 0)
        end = int(image['end'], 0)
        size = image['size']

        m = {
            'id': idx,
            'path': path,
            'base': base,
            'end': end,
            'size': size}

        modules.append(m)

    print('[+] Got module info.')


def populate_bbs(data):
    global bbs
    block_sz = 8
    for i in range(0, len(data), block_sz):
        bbs.add(data[i:i + block_sz])


def create_coverage(modules, bbs):
    coverage = {'modules': [], 'blocks': []}
    for module in modules:
        size = module['end'] - module['base']
        coverage['modules'].append('%3d, %#016x, %#016x, %#016x, %#08x, %#08x, %s' % (
            module['id'], module['base'], module['end'], size, 0, 0, module['path']))
    for bb in bbs:
        coverage['blocks'].append(hex(int.from_bytes(bb[0:8], byteorder='little')))
    return coverage


def on_message(msg, data):
    # print(msg)
    pay = msg['payload']
    if 'map' in pay:
        maps = pay['map']
        populate_modules(maps)
    else:
        populate_bbs(data)


def sigint(signo, frame):
    print('[!] SIGINT, saving %d blocks to \'%s\'' % (len(bbs), outfile))

    dump_coverage()

    print('[!] Done')

    sys.exit(1)


def dump_coverage():
    coverage = create_coverage(modules, bbs)
    pprint.pprint(coverage)
    # if we want to dump to a file -
    # with open(outfile, 'w') as output_file:
    #     output_file.write(coverage)


def main():
    global outfile

    parser = argparse.ArgumentParser()
    parser.add_argument('target',
                        help='target process name or pid',
                        default='-1')
    parser.add_argument('-D', '--device',
                        help='select a device by id [local]',
                        default='local')

    args = parser.parse_args()

    device = frida.get_device(args.device)

    target = -1
    for p in device.enumerate_processes():
        if args.target in [str(p.pid), p.name]:
            if target == -1:
                target = p.pid
            else:
                print('[-] Warning: multiple processes on device match '
                      '\'%s\', using pid: %d' % (args.target, target))

    if target == -1:
        print('[-] Error: could not find process matching '
              '\'%s\' on device \'%s\'' % (args.target, device.id))
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint)

    whitelist_modules = ['all']
    if len(args.whitelist_modules):
        whitelist_modules = args.whitelist_modules

    threadlist = ['all']
    if len(args.thread_id):
        threadlist = args.thread_id

    json_whitelist_modules = json.dumps(whitelist_modules)
    json_threadlist = json.dumps(threadlist)

    print('[*] Attaching to pid \'%d\' on device \'%s\'...' %
          (target, device.id))

    session = device.attach(target)
    print('Loading script')

    script = session.create_script(SCRIPT % (json_whitelist_modules, json_threadlist))
    script.on('message', on_message)
    script.load()
    sys.stdin.read()
    session.detach()
    dump_coverage()

    print('[!] Done')
    sys.exit(0)


if __name__ == '__main__':
    main()
