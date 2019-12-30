from .globals import (
    CONFIG_FILE_NAME
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

keep_alive_channels = []

# ==================================[ callbacks ]==================================
def signal_buffer_opened_cb(data, signal, signal_data):
    global options
    buffer = signal_data
    apply_options_for_buffer(buffer)
    return weechat.WEECHAT_RC_OK

def signal_hotlist_changed_cb(data, signal, signal_data):
    global options
    buffer = signal_data
    script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
    short_name = weechat.buffer_get_string(buffer, "short_name")
    notify_level = weechat.buffer_get_integer(buffer, "notify")
    if script_name == "matrix" and notify_level > 0:
        weechat.buffer_set(buffer, "hidden", "0")
    elif script_name == "matrix" and notify_level <= 0:
        weechat.buffer_set(buffer, "hidden", "1")
    return weechat.WEECHAT_RC_OK

# ==================================[ funcs ]==================================

def get_favorites(buffer):
    favorites = weechat.config_get("%s.buffer.favorites" % CONFIG_FILE_NAME)
    favorites = weechat.config_string(favorites)
    return favorites.split(',')

def apply_options_for_buffer(buffer):
    full_name = weechat.buffer_get_string(buffer, "full_name")
    short_name = weechat.buffer_get_string(buffer, "short_name")
    script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")

    favorites = get_favorites(buffer)

    if short_name not in favorites and script_name == "matrix":
        maybe_hide_buffer(buffer)
    handle_hotlist

def maybe_hide_buffer(buffer):
    if buffer_is_hideable(buffer):
        # weechat.prnt("", "HIDING: %s" % weechat.buffer_get_string(buffer, "short_name"))
        weechat.buffer_set(buffer, "hidden", "1")

def buffer_is_hideable(buffer):
    """Check if passed buffer can be hidden.

    If configuration option ``hide_private`` is enabled,
    private buffers will become hidden as well.

    If the previous buffer name matches any of the exemptions defined in ``exemptions``,
    it will not become hidden.

    :param buffer: Buffer string representation
    """
    if buffer == weechat.current_buffer():
        return False

    buffer_type = weechat.buffer_get_string(buffer, "localvar_type")

    if buffer_type == "server":
        return False

    """
    buffer_type = weechat.buffer_get_string(buffer, 'localvar_type')

    if (buffer_type == "private"
            and weechat.config_get_plugin("hide_private") == "off"):
        return False
    """

    return True


def handle_hotlist():
    global keep_alive_channels
    hotlist_buffers = weechat.infolist_get("hotlist", "", "")

    if not hotlist_buffers:
        return weechat.WEECHAT_RC_OK

    while True:
        buffer = weechat.infolist_pointer(hotlist_buffers, "buffer_pointer")
        full_name = weechat.buffer_get_string(buffer, "full_name")
        short_name = weechat.buffer_get_string(buffer, "short_name")
        script_name = weechat.buffer_get_string(buffer, "localvar_script_name")
        if script_name == "matrix":
            weechat.buffer_set(buffer, "hidden", "0")
            keep_alive_channels.append(full_name)
            weechat.prnt("", "BUFFER: %s" % short_name)
        if not weechat.infolist_next(hotlist_buffers):
            break

    weechat.infolist_free(hotlist_buffers)
