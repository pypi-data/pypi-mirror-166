from rich import print

from noldor import check
from noldor.validators.integer import is_prime, multiple_of

if __name__ == "__main__":
    # Example usage of the library
    response = check(17, is_prime(), multiple_of(1))
    print("\n".join(response.log))
