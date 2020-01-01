from .globals import (
    CONFIG_FILE_NAME
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

#! Entry Point for Weechat Functions (Except for completion, look in command.py for auto-complete)

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

def config_buffer_create_option_cb(data, config_file, section, option_name,
                                   value):
    option = weechat.config_search_option(config_file, section, option_name)
    if option:
        return weechat.config_option_set(option, value, 1)
    else:
        option = weechat.config_new_option(config_file, section, option_name,
                                           "string", "", "", 0, 0, "",
                                           value, 0, "", "", "", "", "", "")
        if not option:
            return weechat.WEECHAT_CONFIG_OPTION_SET_ERROR
        return weechat.WEECHAT_CONFIG_OPTION_SET_OK_SAME_VALUE

def config_reload_cb(data, config_file):
    """Reload configuration file."""
    return weechat.config_reload(config_file)

def config_option_cb(data, option, value):

    if not weechat.config_get(option):  # option was deleted
        return weechat.WEECHAT_RC_OK

    option = option[len("%s.buffer." % CONFIG_FILE_NAME):]

    pos = option.rfind(".")
    if pos > 0:
        buffer_mask = option[0:pos]
        property = option[pos+1:]
        if buffer_mask and property:
            buffers = weechat.infolist_get("buffer", "", buffer_mask)

            if not buffers:
                return weechat.WEECHAT_RC_OK

            while weechat.infolist_next(buffers):
                buffer = weechat.infolist_pointer(buffers, "pointer")
                weechat.buffer_set(buffer, property, value)

            weechat.infolist_free(buffers)

    return weechat.WEECHAT_RC_OK
