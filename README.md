# challenge-django
Projeto simples de api REST usando django 

A api conta com 3 endpoints, abaixo são descritos o padrão de dados a serem passados para cada um:

/signup (post)

{
        "first_name": "test_name",
        "last_name": "test_last_name",
        "e_mail": "test@gmail.com",
        "password": "12345",
				"phone": 12345678,
				"area_code": 81,
				"country_code": "+55"
}

/signin (post)

{
        "e_mail": "test@gmail.com",
        "password": "12345"
}

/me (get)
> token gerado através do login passado através do header
