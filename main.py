import_ok = True

import logging

from matrix_ui.callbacks import (
    config_buffer_create_option_cb,
    config_reload_cb,
    config_option_cb,
    signal_hotlist_changed_cb,
    signal_buffer_opened_cb,
    signal_buffer_switched_cb,
    signal_buffer_changed_cb
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
    SCRIPT_SHORT_HELP,
    SCRIPT_HELP,
    SCRIPT_COMMAND,
    CONFIG_FILE_NAME,
    LOG_LEVEL,
    BUFFERS,
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
    logging.basicConfig(level=LOG_LEVEL, filename='.weechat/wui.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.info("Logging Initiated")
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
                SCRIPT_DESC,
                SCRIPT_SHORT_HELP,
                SCRIPT_HELP,
                "", # autocomplete
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

            weechat.hook_signal("8900|buffer_closed",
                                "signal_buffer_closed_cb", "")

            weechat.hook_signal("8800|buffer_switch",
                                "signal_buffer_switched_cb", "")

            weechat.hook_signal("8700|buffer_renamed",
                                "signal_buffer_changed_cb", "")

            weechat.hook_signal("irc_channel_opened",
                                "signal_buffer_opened_cb", "")

            weechat.hook_signal("hotlist_changed", "signal_hotlist_changed_cb", "")

            weechat.hook_config("%s.buffer.favorites" % CONFIG_FILE_NAME,
                                "config_option_cb", "")

            # apply settings to all already opened buffers
            BUFFERS.refresh()
            weechat.command("", "/key bind meta-t /wui select buffer")
          


# ==================================[ end ]===================================

def unload_script():
    """ Function called when script is unloaded. """
    global config_file

    if config_file:
        config_write()
    return weechat.WEECHAT_RC_OK
