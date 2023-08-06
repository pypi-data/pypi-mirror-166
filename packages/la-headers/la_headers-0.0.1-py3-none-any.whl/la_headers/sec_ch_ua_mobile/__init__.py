from packaging.version import Version

from la_headers.sec_ch_ua_mobile.chromie import CHROME_SEC_CH_UA_MOBILE
from la_headers.sec_ch_ua_mobile.firefox import FIREFOX_SEC_CH_UA_MOBILE
from la_headers.utility import find_best_option

_sec_ch_ua_mobile = {
    "chrome": CHROME_SEC_CH_UA_MOBILE,
    "firefox": FIREFOX_SEC_CH_UA_MOBILE,
}


def generate_sec_ch_ua_mobile(browser: str, version: str, device: str) -> str:
    options = _sec_ch_ua_mobile[browser][device]
    best_option = find_best_option(version, options)

    return best_option
