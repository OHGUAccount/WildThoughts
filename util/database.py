import json
import random

from django.contrib.auth.models import User
from django.core.management import execute_from_command_line
from django.utils.text import slugify

from wildthoughts.models import Animal, Discussion, Petition, UserList, UserProfile


class Database:
    # class dedicated to populate and migrate database
    FILES = ["db.sqlite3"]
    FOLDERS = ["wildthoughts\\migrations"]
    
    animal_dict: dict = None
    profile_dict: dict = None
    adjectives = ['scariest', 'gorgeous', 'fastest', 'slowest']
    animals: list[Animal] = None
    users: list[UserProfile] = None

    @classmethod
    def load_profile_dict(cls) -> dict:
        if not cls.profile_dict:
            with open("profile.json", "r") as f:
                cls.profile_dict = json.load(f)
        return cls.profile_dict

    @classmethod
    def load_animal_dict(cls) -> dict:
        if not cls.animal_dict:
            with open("animal.json", "r") as f:
                cls.animal_dict = json.load(f)
        return cls.animal_dict

    @classmethod
    def load_author(cls) -> UserProfile:
        author, created = User.objects.get_or_create(
            username='animalcorner',
            email='animalcorner@gmail.com',
            password='WAD2Test2024',
        )
        author, created = UserProfile.objects.get_or_create(user=author)
        return author
    
    @classmethod
    def add_users(cls) -> None:
        profile_dict = cls.load_profile_dict()
        for username, data in profile_dict.items():
            user, created = User.objects.get_or_create(
                username = username,
                email = data['email'],
                password = data['password'],
            )

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.picture = data['image_path']
            user_profile.save()

    @classmethod
    def add_animals(cls) -> None:
        animal_dict = cls.load_animal_dict()
        author = cls.load_author()
        for name, data in animal_dict.items():
            animal, created = Animal.objects.get_or_create(
                name=name,
                author=author,
                slug=slugify(name)
            )
            animal.description = data['description']
            animal.picture = data['image_path']
            animal.votes = random.randint(0, 50)
            animal.save()

    @classmethod
    def random_animal(cls) -> Animal:
        if not cls.animals:
            cls.animals = list(Animal.objects.all().order_by('?'))
        return cls.animals.pop()

    @classmethod
    def random_user(cls) -> UserProfile:
        if not cls.users:
            cls.users = list(UserProfile.objects.all().order_by('?'))
        return cls.users.pop()

    @classmethod
    def random_zip(cls, size=5) -> tuple[tuple[UserProfile, Animal]]:
        output_zip = [(cls.random_user(), cls.random_animal()) for i in range(size)]
        return output_zip

    @classmethod
    def add_discussions(cls) -> None:
        for user, animal in cls.random_zip():
            discussion, created = Discussion.objects.get_or_create(
                title=f"Why do you like {animal.name} by {user.user.username}?",
                author=user,
                animal=animal,
                slug=slugify(f"Why do you like {animal.name} by {user.user.username}?")
            )
            discussion.votes = random.randint(0, 50)
            discussion.save()

    @classmethod
    def add_user_lists(cls) -> None:
        users = [cls.random_user() for i in range(5)]
        animals = [cls.random_animal() for i in range(5)]
        for user in users:
            adjective = random.choice(cls.adjectives)
            user_list, created = UserList.objects.get_or_create(
                title=f'Top {adjective} animals by {user.user.username}',
                author=user,
                slug=slugify(f'Top {adjective} animals by {user.user.username}')
            )
            for animal in animals:
              user_list.animals.add(animal)

            user_list.votes = random.randint(0, 50)
            user_list.save()

    @classmethod
    def add_petitions(cls) -> None:
        for user, animal in cls.random_zip():
            petition, created = Petition.objects.get_or_create(
                title=f'Petition for {animal.name} by {user.user.username}',
                author=user,
                picture=animal.picture,
                description="This animal is at the risk of extinction!",
                slug=slugify(f'Petition for {animal.name} by {user.user.username}')
            )
            petition.goal = 100
            petition.signatures = random.randint(0, 50)
            petition.animals.add(animal)
            petition.save()

    @classmethod
    def populate(cls) -> None:
        cls.add_animals()
        cls.add_users()
        cls.add_discussions()
        cls.add_user_lists()
        cls.add_petitions()
        print("Populated the database!")
        
    @classmethod
    def migrate(cls) -> None:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrated the database!")