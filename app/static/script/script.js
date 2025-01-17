async function loginFunction(event) {
                    event.preventDefault();  // Предотвращаем стандартное действие формы

                    // Получаем форму и собираем данные из неё
                    const form = document.getElementById('login-form');
                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData.entries());

                    try {
                        const response = await fetch('/api/login_user', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(data)
                        });

                        // Проверяем успешность ответа
                        if (!response.ok) {
                            // Получаем данные об ошибке
                            const errorData = await response.json();
                            displayErrors(errorData);  // Отображаем ошибки
                            return;  // Прерываем выполнение функции
                        }

                        const result = await response.json();

                        if (result.message) {  // Проверяем наличие сообщения о успешной регистрации
                            window.location.href = '/catalog';  // Перенаправляем пользователя на страницу
                        } else {
                            alert(result.message || 'Неизвестная ошибка');
                        }
                    } catch (error) {
                        console.error('Ошибка:', error);
                        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
                    }
                }

async function logoutFunction() {
    try {
        // Отправка POST-запроса для удаления куки на сервере
        let response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Проверка ответа сервера
        if (response.ok) {
            // Перенаправляем пользователя на страницу логина
            window.location.href = '/login';
        } else {
            // Чтение возможного сообщения об ошибке от сервера
            const errorData = await response.json();
            console.error('Ошибка при выходе:', errorData.message || response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети', error);
    }
}

async function authFunction() {
                try {
                    // Отправка GET-запроса для проверки авторизации пользователя на сервере
                    let response = await fetch('/api/me', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    // Проверка ответа сервера
                    if (!response.ok) {
                        // Перенаправляем пользователя на страницу логина
                        window.location.href = '/login';

                    } else if(response.ok) {
                     // Перенаправляем пользователя на страницу каталога
                        window.location.href = '/catalog';
                    }  else {
                        // Чтение возможного сообщения об ошибке от сервера
                        const errorData = await response.json();
                        console.error('Ошибка при выходе:', errorData.message || response.statusText);
                    }
                } catch (error) {
                    console.error('Ошибка сети', error);
                }
            }

