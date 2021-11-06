import sys

class Output:
    def __init__(self, lnd):
        self.lnd = lnd

    @staticmethod
    def print_line(message, end="\n"):
        sys.stdout.write(f"{message}{end}")

    @staticmethod
    def print_without_linebreak(message):
        sys.stdout.write(message)

    def print_route(self, route):
        route_str = "\n".join(
            self.get_channel_representation(h.chan_id, h.pub_key)
            + "\t"
            + self.get_fee_information(h, route)
            for h in route.hops
        )
        self.print_line(route_str)

    def get_channel_representation(self, chan_id, pubkey_to, pubkey_from=None):
        channel_id_formatted = format_channel_id(chan_id)
        if pubkey_from:
            alias_to_formatted = format_alias(self.lnd.get_node_alias(pubkey_to))
            alias_from = format_alias(self.lnd.get_node_alias(pubkey_from))
            return f"{channel_id_formatted} ({alias_from} to {alias_to_formatted})"
        alias_to_formatted = format_alias(f"{self.lnd.get_node_alias(pubkey_to):32}")
        return f"{channel_id_formatted} to {alias_to_formatted}"

    def get_fee_information(self, next_hop, route):
        hops = list(route.hops)
        if hops[0] == next_hop:
            ppm = self.lnd.get_ppm_to(next_hop.chan_id)
            return f"(free, we usually charge {format_ppm(ppm)})"
        hop = hops[hops.index(next_hop) - 1]
        ppm = int(hop.fee_msat * 1_000_000 / hop.amt_to_forward_msat)
        fee_formatted = "fee " + f"{hop.fee_msat:8,} mSAT"
        ppm_formatted = format_ppm(ppm, 5)
        return f"({fee_formatted}, {ppm_formatted})"


def format_alias(alias):
    if sys.stdout.encoding and not sys.stdout.encoding.lower().startswith("utf"):
        alias = alias.encode("latin-1", "ignore").decode()
    return alias


def format_ppm(ppm, min_length=None):
    if min_length:
        return f"{ppm:{min_length},}ppm"
    return f"{ppm:,}ppm"


def format_fee_msat(fee_msat, min_length=None):
    if min_length:
        return f"{fee_msat:{min_length},} mSAT"
    return f"{fee_msat:,} mSAT"


def format_fee_msat_red(fee_msat, min_length=None):
    if min_length:
        return f"{fee_msat:{min_length},} mSAT"
    return f"{fee_msat:,} mSAT"


def format_fee_sat(fee_sat):
    return f"{fee_sat:,} sats"


def format_earning(msat, min_width=None):
    if min_width:
        return f"{msat:{min_width},} mSAT"
    return f"{msat:,} mSAT"


def format_amount(amount, min_width=None):
    if min_width:
        return f"{amount:{min_width},}"
    return f"{amount:,}"


def format_amount_green(amount, min_width=None):
    return f"{amount:{min_width},}"


def format_boring_string(string):
    return string


def format_success(string):
    return string


def format_channel_id(channel_id):
    return channel_id


def format_warning(warning):
    return warning


def format_error(error):
    return error


def print_bar(width, length):
    result = "["
    if sys.stdout.encoding.lower().startswith("utf"):
        for _ in range(0, length):
            result += "\u2588"
        for _ in range(length, width):
            result += "\u2591"
    else:
        for _ in range(0, length):
            result += "X"
        for _ in range(length, width):
            result += "."
    result += "]"
    return result