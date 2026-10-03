import sender_stand_request
import data

def get_user_body(name):
    current_body= data.user_body.copy()
    current_body['firstName'] = name
    return current_body

def positive_assert(name):
    user_body = get_user_body(name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 201
    assert response.json()['authToken'] != ""

    user_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + response.json()["authToken"]

    assert user_table_response.text.count(str_user) == 1

def negative_assert(name):
    user_body = get_user_body(name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400



def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

def test_create_user_1_letter_in_first_name_get_failed_response():
    negative_assert("A")

def test_create_user_16_letter_in_first_name_get_failed_response():
    negative_assert("Aaaaaaaaaaaaaaaa")

def test_create_user_with_blank_space_letter_in_first_name_get_failed_response():
    negative_assert("A aaa")

def test_create_user_especial_simbol_in_first_name_get_failed_response():
    negative_assert("\"¡%@\",")

def test_create_user_has_number_in_first_name_get_error_response():
        negative_assert("456")

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400

    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"


def test_create_user_no_first_name_get_failed_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

def test_create_user_empty_first_name_get_failed_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_failed_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400








