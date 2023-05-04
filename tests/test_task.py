from api import PetFriends
from settings import valid_email, valid_password
import os
import string
import random

#  генерация рандомной стоки в разном регистре с цифрами, param: k= указать длину строки
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))

#  генерация рандомной последовательности чисел param: range(указать кол-во последовательности)
sequence = int(''.join(random.choice('0123456789') for _ in range(1000)))

pf = PetFriends()


def test_get_api_key_for_invalid_user(email: str = 'zharov@gmail.com', password: str = valid_password):
    """Проверяем запрос с невалидным email и с валидным password.
    Проверяем нет ли ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'


def test_get_api_key_for_invalid_password(email: str = valid_email, password: str = 'Qwertyuiop123'):
    """Проверяем запрос с невалидным password и с валидным email.
    Проверяем нет ли ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'


def test_update_self_pet_invalid_name_str(name: str = ran, animal_type: str = 'Cat', age: int = 5):
    """Проверка с негативным сценарием.
    Поле имя не должно принимать на ввод более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['name']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_invalid_name_int(name: int = 4, animal_type: str = 'Dog', age: int = 10):
    """Проверка с негативным сценарием.
    Поле имя не должно принимать цифры в любом виде"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, имя питомца указано в буквенном значении
        assert status == 200
        assert result['name'].isalpha(), 'Имя животного не может быть цифрой'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_invalid_animal_type(name: str = 'Борис', animal_type: str = ran, age: int = 5):
    """Проверка с негативным сценарием.
     Поле порода не должно принимать на ввод более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['animal_type']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_invalid_age(name: str = 'Борис', animal_type: str = 'Персидская', age: int = 101):
    """Проверка с негативным сценарием.
    Поле возраст не должно принимать более двух цифр в возрасте питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['age']) < 3, 'Возраст животного не может быть трехзначной цифрой'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_big_photo_jpeg(pet_photo: str = 'images/chernyj_kot_size_3840x2400.jpg'):
    """Проверка с позитивным сценарием.
    Обновление фото в HD разрешении 3840x2400, формат jpeg"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200, 'Формат jpeg в высоком разрешении не принимается сайтом '
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_photo_png(pet_photo: str = 'images/Green-Alligator-Transparent-PNG.png'):
    """Проверка с позитивным сценарием.
    Возможность обновления фото в формате png"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200, 'Формат png не поддерживается'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_invalid_animal_type_int(name: str = 'Ivanco', animal_type: int = 5, age: int = 10):
    """Проверка с негативным сценарием.
      Поле порода не должно принимать цифры в любом виде"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, вид питомца указано в буквенном значении
        assert status == 200
        assert result['animal_type'].isalpha(), 'Поле порода не должно содержвть цифр'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_update_self_pet_empty_data(name: any = '', animal_type: any = '', age: any = ''):
    """Проверка с негативным сценарием.
    Оставляем все поля пустыми, форма их принимает и заводит питомца с пустыми данными."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом, поля не должны приниматься пустыми
    assert status == 200
    assert result['name'] != '', 'Поле имя не должно быть пустым'
    assert result['animal_type'] != '', 'Поле порода не должно быть пустым'
    assert result['age'] != '', 'Поле возраст не должно быть пустым'

