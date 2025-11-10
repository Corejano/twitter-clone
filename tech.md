# Техническое задание: Клон Twitter

## 1. Общее описание проекта

Разработка веб-приложения - клона социальной сети Twitter с базовым функционалом публикации постов, ленты новостей, профилей пользователей и приватного чата между пользователями.

## 2. Технологический стек

### Backend
- **Framework**: Django REST Framework (DRF)
- **База данных**: PostgreSQL
- **Язык**: Python 3.11+

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Язык**: TypeScript (рекомендуется) или JavaScript

### Инфраструктура
- **Контейнеризация**: Docker, Docker Compose
- **Web-сервер**: Nginx (для production)

### Дополнительные технологии
- **WebSockets**: Django Channels (для real-time чата)
- **Кэширование**: Redis (для сессий и WebSocket)
- **Аутентификация**: JWT (djangorestframework-simplejwt)

## 3. Принципы разработки

- **ООП** - объектно-ориентированное программирование
- **DRY** - Don't Repeat Yourself (избегать дублирования кода)
- **SOLID** - следование принципам проектирования
- **Separation of Concerns** - разделение ответственности
- **Маппинг данных** - использование serializers (DRF) и mappers для преобразования данных
- **Clean Architecture** - чистая архитектура с разделением слоев

## 4. Функциональные требования

### 4.1. Аутентификация и авторизация

#### 4.1.1. Регистрация пользователя
- Поля: username (уникальный), email (уникальный), password, full_name
- Валидация:
  - Username: 3-15 символов, только буквы, цифры и подчеркивание
  - Email: стандартная валидация email
  - Password: минимум 8 символов
- После регистрации автоматический вход в систему

#### 4.1.2. Вход в систему
- Авторизация по username/email и password
- Выдача JWT токенов (access и refresh)
- Возможность "Remember me"

#### 4.1.3. Выход из системы
- Инвалидация токенов

#### 4.1.4. Восстановление пароля
- По email (опционально для MVP)

### 4.2. Профиль пользователя

#### 4.2.1. Просмотр профиля
- Публичная информация:
  - Username
  - Full name
  - Bio (описание, до 160 символов)
  - Avatar (изображение профиля)
  - Header image (фоновое изображение)
  - Дата регистрации
  - Количество подписчиков (followers)
  - Количество подписок (following)
  - Количество постов
- Лента постов пользователя
- Вкладки: Posts, Replies (опционально), Media (опционально), Likes

#### 4.2.2. Редактирование профиля
- Редактирование всех полей профиля (кроме username)
- Загрузка и обрезка изображений (avatar, header)
- Ограничения: avatar до 2MB, header до 5MB

#### 4.2.3. Система подписок
- Кнопка "Follow/Unfollow"
- Список подписчиков (Followers)
- Список подписок (Following)
- Счетчики подписчиков/подписок

### 4.3. Посты (Tweets)

#### 4.3.1. Создание поста
- Текст поста: до 280 символов
- Прикрепление изображений: до 4 изображений
- Счетчик символов
- Предпросмотр изображений перед публикацией
- Кнопка "Post"

#### 4.3.2. Просмотр постов
- Отображение информации:
  - Автор (avatar, full name, username)
  - Время публикации (относительное: "2h ago", "1d ago")
  - Текст поста
  - Прикрепленные изображения (галерея)
  - Счетчики: лайки, ретвиты (опционально), ответы (опционально)

#### 4.3.3. Взаимодействие с постами
- **Like/Unlike**: лайк/дизлайк поста
- **Retweet** (опционально): репост с/без комментария
- **Reply** (опционально): ответ на пост
- **Delete**: удаление собственного поста

#### 4.3.4. Лента постов (Feed)
- **Home Feed**: посты от пользователей, на которых подписан + собственные посты
- Сортировка: по времени публикации (новые сверху)
- Бесконечная прокрутка (infinite scroll) или пагинация
- Автоматическое обновление при появлении новых постов (опционально)

#### 4.3.5. Просмотр отдельного поста
- Страница с детальным просмотром поста
- Список ответов (если реализованы)

### 4.4. Чат между пользователями

#### 4.4.1. Список чатов (Messages)
- Список всех диалогов
- Отображение:
  - Avatar собеседника
  - Имя собеседника
  - Последнее сообщение (превью)
  - Время последнего сообщения
  - Индикатор непрочитанных сообщений
- Сортировка по времени последнего сообщения

#### 4.4.2. Окно чата
- Отображение истории сообщений
- Информация о собеседнике вверху (avatar, name, username)
- Разделение на отправленные/полученные сообщения
- Временные метки для каждого сообщения

#### 4.4.3. Отправка сообщений
- Поле ввода текста
- Кнопка отправки
- Real-time доставка через WebSocket
- Отображение статуса "typing..." (опционально)
- Возможность отправки изображений (опционально)

#### 4.4.4. Создание нового чата
- Поиск пользователей по username
- Кнопка "New Message"
- Начало диалога с выбранным пользователем

### 4.5. Поиск

#### 4.5.1. Поиск пользователей
- Поиск по username и full name
- Отображение результатов с avatar, именем, username
- Возможность перехода в профиль и подписки

#### 4.5.2. Поиск постов (опционально)
- Поиск по содержимому постов
- Полнотекстовый поиск

### 4.6. Уведомления (опционально для MVP)
- Уведомления о новых подписчиках
- Уведомления о лайках
- Уведомления об ответах

## 5. Нефункциональные требования

### 5.1. Производительность
- Время загрузки страницы: не более 2 секунд
- API response time: не более 500ms для основных запросов
- Поддержка одновременной работы минимум 100 пользователей

### 5.2. Масштабируемость
- Возможность горизонтального масштабирования через Docker
- Оптимизация запросов к БД (select_related, prefetch_related)
- Индексы на часто запрашиваемые поля

### 5.3. Безопасность
- HTTPS для production
- Защита от SQL-инъекций (ORM Django)
- Защита от XSS атак
- CSRF токены
- Rate limiting для API endpoints
- Валидация и санитизация всех входных данных
- Хеширование паролей (bcrypt/argon2)

### 5.4. Юзабилити
- Адаптивный дизайн (responsive design)
- Поддержка основных браузеров: Chrome, Firefox, Safari, Edge (последние 2 версии)
- Минимальное разрешение: 320px (mobile)

### 5.5. Надежность
- Обработка ошибок на backend и frontend
- Логирование ошибок
- Graceful degradation при недоступности сервисов

## 6. Архитектура системы

### 6.1. Backend Architecture

#### 6.1.1. Структура приложений Django
```
backend/
├── apps/
│   ├── users/          # Управление пользователями
│   ├── posts/          # Посты и взаимодействия
│   ├── chat/           # Чат и сообщения
│   └── core/           # Общие компоненты
├── config/             # Настройки проекта
└── manage.py
```

#### 6.1.2. Слои приложения
- **Models**: определение моделей данных
- **Serializers**: маппинг данных для API (input/output)
- **Services**: бизнес-логика (слой сервисов)
- **Views/ViewSets**: обработка HTTP запросов
- **Permissions**: кастомные права доступа
- **Validators**: кастомные валидаторы

#### 6.1.3. Модели данных

**User (расширение AbstractUser)**
- id: UUID (primary key)
- username: CharField (unique)
- email: EmailField (unique)
- full_name: CharField
- bio: TextField (blank=True)
- avatar: ImageField (blank=True)
- header_image: ImageField (blank=True)
- date_joined: DateTimeField (auto)
- is_verified: BooleanField (для "галочки")

**Follow**
- id: BigAutoField
- follower: ForeignKey(User) - кто подписался
- following: ForeignKey(User) - на кого подписались
- created_at: DateTimeField (auto)
- Unique constraint: (follower, following)

**Post**
- id: UUID (primary key)
- author: ForeignKey(User)
- content: TextField (max_length=280)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
- likes_count: IntegerField (denormalized)
- retweets_count: IntegerField (denormalized, optional)
- replies_count: IntegerField (denormalized, optional)

**PostImage**
- id: BigAutoField
- post: ForeignKey(Post)
- image: ImageField
- order: IntegerField (для сортировки)

**Like**
- id: BigAutoField
- user: ForeignKey(User)
- post: ForeignKey(Post)
- created_at: DateTimeField (auto)
- Unique constraint: (user, post)

**Chat**
- id: UUID (primary key)
- participants: ManyToManyField(User)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)

**Message**
- id: UUID (primary key)
- chat: ForeignKey(Chat)
- sender: ForeignKey(User)
- content: TextField
- created_at: DateTimeField (auto)
- is_read: BooleanField (default=False)

### 6.2. Frontend Architecture

#### 6.2.1. Структура проекта Vue
```
frontend/
├── src/
│   ├── components/     # Переиспользуемые компоненты
│   ├── views/          # Страницы (роуты)
│   ├── composables/    # Composition API логика
│   ├── services/       # API сервисы
│   ├── stores/         # Pinia stores (state management)
│   ├── types/          # TypeScript типы
│   ├── utils/          # Утилиты
│   ├── router/         # Vue Router
│   ├── assets/         # Статические ресурсы
│   └── App.vue
```

#### 6.2.2. Основные компоненты
- **Layout components**: Navbar, Sidebar, MobileNav
- **Post components**: PostCard, PostForm, PostDetail
- **User components**: UserCard, ProfileHeader, UserList
- **Chat components**: ChatList, ChatWindow, MessageBubble
- **Common components**: Button, Input, Modal, Avatar, ImageGallery

#### 6.2.3. State Management (Pinia)
- **authStore**: аутентификация, текущий пользователь
- **postsStore**: лента постов, создание/удаление
- **profileStore**: данные профиля, подписки
- **chatStore**: список чатов, сообщения
- **uiStore**: состояние UI (модалки, загрузки)

### 6.3. API Design

#### 6.3.1. REST API Endpoints

**Authentication**
- POST `/api/auth/register/` - регистрация
- POST `/api/auth/login/` - вход
- POST `/api/auth/logout/` - выход
- POST `/api/auth/token/refresh/` - обновление токена

**Users**
- GET `/api/users/me/` - текущий пользователь
- PATCH `/api/users/me/` - обновление профиля
- GET `/api/users/{username}/` - профиль пользователя
- GET `/api/users/{username}/posts/` - посты пользователя
- GET `/api/users/{username}/followers/` - подписчики
- GET `/api/users/{username}/following/` - подписки
- POST `/api/users/{username}/follow/` - подписаться
- DELETE `/api/users/{username}/follow/` - отписаться
- GET `/api/users/search/?q=query` - поиск пользователей

**Posts**
- GET `/api/posts/` - лента постов (feed)
- POST `/api/posts/` - создать пост
- GET `/api/posts/{id}/` - детальный просмотр поста
- DELETE `/api/posts/{id}/` - удалить пост
- POST `/api/posts/{id}/like/` - лайкнуть
- DELETE `/api/posts/{id}/like/` - убрать лайк
- GET `/api/posts/{id}/likes/` - список лайкнувших

**Chat**
- GET `/api/chats/` - список чатов
- POST `/api/chats/` - создать чат
- GET `/api/chats/{id}/` - детали чата
- GET `/api/chats/{id}/messages/` - сообщения чата
- POST `/api/chats/{id}/messages/` - отправить сообщение
- PATCH `/api/chats/{id}/messages/{msg_id}/read/` - пометить как прочитанное

**WebSocket**
- WS `/ws/chat/{chat_id}/` - real-time чат

#### 6.3.2. Пагинация
- Использовать `PageNumberPagination` или `CursorPagination`
- Стандартный размер страницы: 20 элементов
- Параметры: `?page=1&page_size=20`

#### 6.3.3. Фильтрация и сортировка
- Использовать `django-filter`
- Стандартная сортировка: `-created_at` (новые первыми)

### 6.4. Database Schema

#### 6.4.1. Индексы
- `User.username` - unique index
- `User.email` - unique index
- `Post.author` + `Post.created_at` - composite index
- `Follow.follower` + `Follow.following` - unique composite index
- `Like.user` + `Like.post` - unique composite index
- `Message.chat` + `Message.created_at` - composite index

#### 6.4.2. Оптимизация запросов
- Использовать `select_related()` для ForeignKey
- Использовать `prefetch_related()` для ManyToMany
- Денормализация счетчиков (likes_count, followers_count)
- Обновление через сигналы или методы модели

## 7. Дизайн интерфейса

### 7.1. Общие требования
- **Точное копирование дизайна Twitter** (версия 2023-2024)
- Цветовая схема:
  - Primary: #1DA1F2 (Twitter blue)
  - Background: #FFFFFF (light mode)
  - Text: #0F1419 (primary text)
  - Secondary text: #536471
  - Borders: #EFF3F4
  - Hover states: #F7F9F9

### 7.2. Типографика
- Font family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
- Размеры шрифтов: 15px (основной), 13px (вторичный), 20px (заголовки)
- Font weights: 400 (regular), 700 (bold)

### 7.3. Основные экраны

#### 7.3.1. Home Feed
- Левый сайдбар: навигация (Home, Explore, Messages, Profile)
- Центральная колонка: лента постов с формой создания поста сверху
- Правый сайдбар: поиск, "Who to follow", Trends (опционально)

#### 7.3.2. Profile Page
- Header с фоновым изображением
- Avatar (перекрывает header)
- Кнопка "Edit Profile" или "Follow"
- Информация: name, username, bio, join date, following/followers count
- Табы с постами

#### 7.3.3. Messages
- Двухколоночный layout: список чатов слева, окно чата справа
- На мобильных: переключение между списком и чатом

#### 7.3.4. Post Detail
- Увеличенная карточка поста
- Полная информация о посте
- Список ответов ниже (если реализовано)

### 7.4. Компоненты UI
- Кнопки: скругленные (border-radius: 9999px), hover эффекты
- Карточки постов: border-bottom, padding, hover background
- Модальные окна: центрированные, с backdrop
- Формы: минималистичные, с валидацией
- Аватары: круглые, с fallback на инициалы

### 7.5. Responsive Design
- Desktop: > 1024px (три колонки)
- Tablet: 768px - 1024px (две колонки)
- Mobile: < 768px (одна колонка, bottom navigation)

### 7.6. Анимации и transitions
- Smooth transitions для всех интерактивных элементов
- Fade-in для новых постов
- Slide-in для сайдбаров на мобильных

## 8. DevOps и развертывание

### 8.1. Docker Configuration

#### 8.1.1. Контейнеры
- **backend**: Django приложение
- **frontend**: Vue приложение (dev server) / Nginx (production)
- **db**: PostgreSQL
- **redis**: Redis для кэширования и WebSocket
- **nginx**: Reverse proxy (production)

#### 8.1.2. docker-compose.yml
- Development конфигурация с hot-reload
- Production конфигурация с оптимизацией
- Volume mounts для персистентности данных

### 8.2. Environment Variables
- Использовать `.env` файлы
- Разделение на `.env.development` и `.env.production`
- Переменные:
  - `DATABASE_URL`
  - `SECRET_KEY`
  - `DEBUG`
  - `ALLOWED_HOSTS`
  - `CORS_ALLOWED_ORIGINS`
  - `REDIS_URL`

### 8.3. CI/CD (опционально)
- GitHub Actions для автоматического тестирования
- Линтеры: flake8, black (Python), ESLint, Prettier (Vue)
- Автоматический деплой на staging/production

## 9. Тестирование

### 9.1. Backend Testing
- Unit tests для моделей и сервисов
- Integration tests для API endpoints
- Coverage: минимум 70%
- Использовать `pytest-django`

### 9.2. Frontend Testing
- Unit tests для composables и utils
- Component tests для критичных компонентов
- E2E tests для основных user flows (опционально)
- Использовать Vitest или Jest


### 10.2. README.md
- Описание проекта
- Инструкции по установке и запуску
- Структура проекта
- Основные команды


## 12. Критерии приемки

### 12.1. Функциональность
- ✅ Пользователь может зарегистрироваться и войти в систему
- ✅ Пользователь может редактировать свой профиль
- ✅ Пользователь может создавать посты с текстом и изображениями
- ✅ Пользователь видит ленту постов от подписок
- ✅ Пользователь может лайкать посты
- ✅ Пользователь может подписываться/отписываться от других
- ✅ Пользователь может отправлять личные сообщения
- ✅ Чат работает в real-time
- ✅ Пользователь может искать других пользователей

### 12.2. Дизайн
- ✅ Интерфейс полностью копирует Twitter
- ✅ Адаптивный дизайн на всех устройствах
- ✅ Все интерактивные элементы работают корректно

### 12.3. Технические требования
- ✅ Проект запускается через Docker Compose одной командой
- ✅ Код следует принципам ООП, DRY, SOLID
- ✅ API документирован
- ✅ Базовые тесты написаны и проходят
- ✅ Нет критичных багов и ошибок
