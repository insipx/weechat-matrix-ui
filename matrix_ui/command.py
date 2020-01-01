import_ok = True

from .globals import (
    SCRIPT_COMMAND,
    CONFIG_FILE_NAME
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False

def favorites():
    favorites = weechat.config_get("weechat-matrix-ui.buffer.favorites")
    favorites = weechat.config_string(favorites)
    return favorites.split(',')

def wui_cmd(data, buffer, args):
    """Callback for /buffer_autoset command."""
    args = args.strip()
    if args == "":
        weechat.command("", "/set %s.buffer.*" % CONFIG_FILE_NAME)
        return weechat.WEECHAT_RC_OK
    argv = args.split(None, 3)
    if len(argv) > 0:
        if argv[0] == "add":
            if len(argv) < 2:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            favs = favorites()
            favs.append(argv[1])
            new_val = ','.join(favs)
            weechat.command("", "/set %s.buffer.favorites %s" % (CONFIG_FILE_NAME, new_val))
        elif argv[0] == "del":
            if len(argv) < 2:
                weechat.command("", "/help %s" % SCRIPT_COMMAND)
                return weechat.WEECHAT_RC_OK
            favs = favorites()
            if argv[1] not in favs:
                weechat.prnt("", "%s not in favorites" % argv[1])
                return weechat.WEECHAT_RC_OK
            else:
                favs.remove(argv[1])
                new_val = ','.join(favs)
                weechat.command("", "/set %s.buffer.favorites %s" % (CONFIG_FILE_NAME, new_val))
        else:
            weechat.command("", "/help %s" % SCRIPT_COMMAND)
            return weechat.WEECHAT_RC_OK
    return weechat.WEECHAT_RC_OK


def completion_current_buffer_cb(data, completion_item, buffer,
                                     completion):
    """
    Complete with current buffer name (plugin.name),
    for command '/buffer_autoset'.
    """
    name = "%s.%s" % (weechat.buffer_get_string(buffer, "plugin"),
                      weechat.buffer_get_string(buffer, "name"))
    weechat.hook_completion_list_add(completion, name,
                                     0, weechat.WEECHAT_LIST_POS_BEGINNING)
    return weechat.WEECHAT_RC_OK


def completion_options_cb(data, completion_item, buffer, completion):
    """Complete with config options, for command '/buffer_autoset'."""
    options = weechat.infolist_get("option", "",
                                   "%s.buffer.*" % CONFIG_FILE_NAME)
    if options:
        while weechat.infolist_next(options):
            weechat.hook_completion_list_add(
                completion,
                weechat.infolist_string(options, "option_name"),
                0, weechat.WEECHAT_LIST_POS_SORT)
        weechat.infolist_free(options)
    return weechat.WEECHAT_RC_OK
