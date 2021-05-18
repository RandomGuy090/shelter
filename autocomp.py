import variables  as var
import re, readline




class Completer(object):


    def complete_extra(self, args):
        "Completions for the 'extra' command."
        if not args:
            return self._complete_path('.')
        return self._complete_path(args[-1])

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        if not line:
            return [c + ' ' for c in var.COMMANDS][state]
        
        if re.compile('.*\s+$', re.M).match(buffer):
            line.append('')

        cmd = line[0].strip()
        if cmd in var.COMMANDS:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
        
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        
        results = [c + ' ' for c in var.COMMANDS if c.startswith(cmd)] + [None]
        return results[state]


comp = Completer()
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(comp.complete)