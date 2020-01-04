from .globals import (
    CONFIG_FILE_NAME,
    BUFFERS
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org")
    import_ok = False

#! Entry Point for Weechat Functions (Except for completion, look in command.py for auto-complete)

def signal_buffer_opened_cb(data, signal, signal_data):
    BUFFERS.on_buffer_open(signal_data)
    return weechat.WEECHAT_RC_OK

def signal_buffer_closed_cb(data, signal, signal_data):
    BUFFERS.on_buffer_kill(signal_data)
    return weechat.WEECHAT_RC_OK

def signal_buffer_switched_cb(data, signal, signal_data):
    BUFFERS.on_buffer_switch(signal_data)
    return weechat.WEECHAT_RC_OK

def signal_buffer_changed_cb(data, signal, signal_data):
    BUFFERS.on_buffer_changed(signal_data)
    return weechat.WEECHAT_RC_OK

def signal_hotlist_changed_cb(data, signal, signal_data):
    BUFFERS.on_hotlist_changed(signal_data)
    return weechat.WEECHAT_RC_OK

def config_reload_cb(data, config_file):
    """Reload configuration file."""
    return weechat.config_reload(config_file)

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

def config_option_cb(data, option, value):
    # Refresh buffers when favorites change
    if not weechat.config_get(option):  # option was deleted
        return weechat.WEECHAT_RC_OK
    BUFFERS.refresh()
    return weechat.WEECHAT_RC_OK
