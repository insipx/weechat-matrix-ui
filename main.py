import_ok = True

from matrix_ui._weechat import (
    config_buffer_create_option_cb,
    config_reload_cb,
    config_option_cb,
)

from matrix_ui.buffers import (
    handle_hotlist,
    signal_hotlist_changed_cb,
    signal_buffer_opened_cb
)

from matrix_ui.command import (
    wui_cmd,
    completion_current_buffer_cb,
    completion_options_cb,
)

from matrix_ui.globals import (
    SCRIPT_NAME,
    SCRIPT_AUTHOR,
    SCRIPT_VERSION,
    SCRIPT_LICENSE,
    SCRIPT_DESC,
    SCRIPT_COMMAND,
    CONFIG_FILE_NAME
)

try:
    import weechat
except ImportError:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False


# config file / options
config_file = ""
options = {}

def config_init():
    """
    Initialization of configuration file.
    Sections: buffer.
    """
    global config_file, options
    config_file = weechat.config_new(CONFIG_FILE_NAME,
                                         "config_reload_cb", "")
    if config_file == "":
        return

    # section "buffer"
    section_buffer = weechat.config_new_section(
        config_file, "buffer", 1, 1, "", "", "", "", "", "",
        "config_buffer_create_option_cb", "", "", "")
    if not section_buffer:
        weechat.config_free(config_file)
        return
    options["favorites"] = weechat.config_new_option(
        config_file, section_buffer, "favorites", "string",
        "comma-delimited list of favorite rooms",
        "", 0, 0, "", "", 0, "", "", "", "", "", ""
        )

def config_read():
    """Read configuration file."""
    global config_file
    return weechat.config_read(config_file)

def config_write():
    """Write configuration file."""
    global config_file
    return weechat.config_write(config_file)


# ==================================[ main ]==================================

if __name__ == "__main__" and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                        SCRIPT_LICENSE, SCRIPT_DESC, "unload_script", ""):
        version = weechat.info_get("version_number", "") or 0
        if int(version) < 0x01000000:
            weechat.prnt("", "%s%s: WeeChat 1.0 is required for this script."
                         % (weechat.prefix("error"), SCRIPT_NAME))
        else:
            config_init()
            config_read()
            weechat.hook_command(
                SCRIPT_COMMAND,
                "Hides Matrix Buffers unless there is activity",
                "", "", "",
                "wui_cmd", "")

            """
            weechat.hook_completion(
                "wui_current_buffer",
                "Current buffer name for wui",
                "completion_current_buffer_cb"
            )

            weechat.hook_completion(
                "wui_options",
                "list of options for wui",
                "completion_options_cb"
            )
            """

            weechat.hook_signal("9000|buffer_opened",
                        "signal_buffer_opened_cb", "")

            weechat.hook_signal("hotlist_changed", "signal_hotlist_changed_cb", "")

            weechat.hook_config("%s.buffer.*" % CONFIG_FILE_NAME,
                                "config_option_cb", "")

            handle_hotlist()
            # apply settings to all already opened buffers
            buffers = weechat.infolist_get("buffer", "", "")
            if buffers:
                while weechat.infolist_next(buffers):
                    buffer = weechat.infolist_pointer(buffers, "pointer")
                    signal_buffer_opened_cb("", "", buffer)
                weechat.infolist_free(buffers)


# ==================================[ end ]===================================

def unload_script():
    """ Function called when script is unloaded. """
    global config_file

    if config_file:
        config_write()
    return weechat.WEECHAT_RC_OK
