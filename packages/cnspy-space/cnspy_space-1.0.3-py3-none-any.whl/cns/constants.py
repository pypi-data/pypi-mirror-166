from eth_typing import (
    ChecksumAddress,
    HexAddress,
    HexStr,
)
from hexbytes import (
    HexBytes,
)


ACCEPTABLE_STALE_HOURS = 48

AUCTION_START_GAS_CONSTANT = 25000
AUCTION_START_GAS_MARGINAL = 39000

EMPTY_SHA3_BYTES = HexBytes(b"\0" * 32)
EMPTY_ADDR_HEX = HexAddress(HexStr("0x" + "00" * 20))

REVERSE_REGISTRAR_DOMAIN = "addr.reverse"


CNS_MAINNET_ADDR = ChecksumAddress(
    HexAddress(HexStr("0xec3133E740FcAc8AC7212078522E3Ee3FFde0903"))
)


# --- interface ids --- #

GET_TEXT_INTERFACE_ID = HexStr("0x59d1d43c")
EXTENDED_RESOLVER_INTERFACE_ID = HexStr("0x9061b923")  # ENSIP-10
