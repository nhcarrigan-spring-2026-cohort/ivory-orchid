import os, requests
from .types import Pet, Shelter

inquiry_webhook: str|None = os.getenv("INQUIRY_WEBHOOK")
inquiry_webhook_enabled: bool = inquiry_webhook is not None and inquiry_webhook.strip() != ""

def send_inquiry(data) -> None :
    if inquiry_webhook_enabled:
        requests.post(inquiry_webhook, json=data)

def get_test_pets() -> list[Pet]:
    dog1 = Pet("rex", 10, "male", "calm border-collie", "kripto.jpg", 6.25, "cohort", True, "dog")
    dog2 = Pet("max", 3, "male", "survived a car crash", "dogandcat.jpg", 2.1, "shelterB", True, "dog")
    dog3 = Pet("bella", 1, "female", "loves big walks, needs attention", "kripto.jpg", 6.25, "cohort", True, "dog")

    cat1 = Pet("Snowball", 10, "male", "Full of energy", "dogandcat.jpg", 15, "shelterB", True, "cat")
    cat2 = Pet("fog", 10, "female", "has an interesting color", "snowball.jpg", 3, "cohort", True, "cat")
    cat3 = Pet("sunny", 10, "female", "Very fat", "dogandcat.jpg", 8, "closedShelter", False, "cat")

    return [dog1, dog2, dog3, cat1, cat2, cat3]

def get_test_shelters() -> list[Shelter]:
    shelter_cohort = Shelter("cohort", "ivory-orchid@cohort.org", "+156547896542", "12 rue de Prony, 75017 Paris, France")
    shelter_b = Shelter("shelterB", "shelters@ivory.orchid.org", "+215654789564", "760 United Nations Plaza, New York, NY 10017, USA")
    shelter_closed = Shelter("closedShelter", "automations@example.com","+0123456789","1600 Pennsylvania Ave NW, Washington, DC 20500, USA")

    return [shelter_cohort, shelter_b, shelter_closed]

def setup_db(db):
    """
    Set up the database creating the table if they are missing and seed it with some data unless the enviroment variable DATABASE_SEEDING is set to False
    """
    db.create_all()

    import os
    if os.getenv("DATABASE_SEEDING", "True") == "False":
        return

    first_shelter = Shelter.query.get(1)
    if first_shelter is None:
        db.session.add_all(get_test_shelters())
        db.session.commit()

    first_pet = Pet.query.get(1)
    if first_pet is None:
        db.session.add_all(get_test_pets())
        db.session.commit()
