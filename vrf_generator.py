import argparse
import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Recovered from the rotated string table in heh.js.
VRF_PREFIX = "Cns#nGelOl"


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def generate_vrf(movie_id: str, user_id: str, prefix: str = VRF_PREFIX) -> dict:
    secret = f"{prefix}X_{user_id}"
    key = hashlib.sha256(secret.encode("utf-8")).digest()
    plaintext = pkcs7_pad(movie_id.encode("utf-8"))

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(bytes(16)),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    vrf = (
        base64.b64encode(ciphertext)
        .decode("ascii")
        .replace("+", "-")
        .replace("/", "_")
        .rstrip("=")
    )

    return {
        "movie_id": movie_id,
        "user_id": user_id,
        "prefix": prefix,
        "secret": secret,
        "vrf": vrf,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate vidsrc.cc VRF")
    parser.add_argument("movie_id", nargs="?", default="385687")
    parser.add_argument("user_id", nargs="?", default="BB0IMwUjDHgHMH0wBA0APAcu")
    parser.add_argument("--prefix", default=VRF_PREFIX)
    args = parser.parse_args()

    result = generate_vrf(args.movie_id, args.user_id, args.prefix)
    print(f"movie_id: {result['movie_id']}")
    print(f"user_id:  {result['user_id']}")
    print(f"prefix:   {result['prefix']}")
    print(f"secret:   {result['secret']}")
    print(f"vrf:      {result['vrf']}")


if __name__ == "__main__":
    main()
