import string
import random
import time
import utile.data as data

# valeurs de simulation
fake_victims = []

fake_histories1 = []

fake_histories2 = []

fake_histories3 = []

fake_histories4 = []

fake_histories = {
    1: fake_histories1,
    2: fake_histories2,
    3: fake_histories3,
    4: fake_histories4
}


def simulate_key(longueur=0):
    letters = ".éèàçùµ()[]" + string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(longueur))


def simulate_hash(longueur=0):
    letters = string.hexdigits
    return ''.join(random.choice(letters) for i in range(longueur))


def main():
    # Ajoute de fausses données dans la DB pour les tests
    exit(0)

if __name__ == '__main__':
    main()
