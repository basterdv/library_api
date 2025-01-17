from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

AuthorAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Автор уже существует')

AuthorNotExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Автор НЕ существует')

BookAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Книга уже существует')

BookANotExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Книга не существует')

BookOutOfStock = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Книга отсутствует на складе')

CountBookExceeded  = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                   detail='Количество выдаваемых книг не должно превышать 5 штук.')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Токен истек')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Токен истек')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')