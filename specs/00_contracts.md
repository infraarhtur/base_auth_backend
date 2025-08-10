# Database Contract

This document describes the database schema for the authentication and authorization system. It defines all tables, columns, data types, default values, and constraints.

## Schema: `public`

### Table: `app_user`

| Column           | Type      | Description                                                      |
| ---------------- | --------- | ---------------------------------------------------------------- |
| id               | UUID      | Primary key, auto-generated                                      |
| name             | TEXT      | Name of the user                                                 |
| email            | TEXT      | Unique email of the user                                         |
| hashed\_password | TEXT      | Hashed user password                                             |
| is\_active       | BOOLEAN   | Indicates if the user is active, default `true`                  |
| created\_at      | TIMESTAMP | Timestamp when the user was created, default `CURRENT_TIMESTAMP` |

### Table: `company`

| Column      | Type      | Description                                                         |
| ----------- | --------- | ------------------------------------------------------------------- |
| id          | UUID      | Primary key, auto-generated                                         |
| name        | TEXT      | Name of the company                                                 |
| created\_at | TIMESTAMP | Timestamp when the company was created, default `CURRENT_TIMESTAMP` |

### Table: `permission`

| Column | Type | Description                   |
| ------ | ---- | ----------------------------- |
| id     | UUID | Primary key, auto-generated   |
| name   | TEXT | Unique name of the permission |

### Table: `company_user`

| Column      | Type | Description                   |
| ----------- | ---- | ----------------------------- |
| company\_id | UUID | Foreign key to `company(id)`  |
| user\_id    | UUID | Foreign key to `app_user(id)` |

**Primary key:** (`company_id`, `user_id`)

### Table: `role`

| Column      | Type | Description                          |
| ----------- | ---- | ------------------------------------ |
| id          | UUID | Primary key, auto-generated          |
| company\_id | UUID | Foreign key to `company(id)`         |
| name        | TEXT | Name of the role, unique per company |

**Constraints:**

* Unique `(company_id, name)`

### Table: `role_permission`

| Column         | Type | Description                     |
| -------------- | ---- | ------------------------------- |
| role\_id       | UUID | Foreign key to `role(id)`       |
| permission\_id | UUID | Foreign key to `permission(id)` |

**Primary key:** (`role_id`, `permission_id`)

### Table: `user_identity`

| Column             | Type      | Description                                                        |
| ------------------ | --------- | ------------------------------------------------------------------ |
| id                 | UUID      | Primary key, auto-generated                                        |
| user\_id           | UUID      | Foreign key to `app_user(id)`                                      |
| provider           | TEXT      | Name of the identity provider (e.g., Google)                       |
| provider\_user\_id | TEXT      | Unique ID from the provider                                        |
| email              | TEXT      | Email from provider (optional)                                     |
| name               | TEXT      | Name from provider (optional)                                      |
| created\_at        | TIMESTAMP | Timestamp when the identity was added, default `CURRENT_TIMESTAMP` |

**Constraints:**

* Unique `(provider, provider_user_id)`

### Table: `user_role`

| Column   | Type | Description                   |
| -------- | ---- | ----------------------------- |
| user\_id | UUID | Foreign key to `app_user(id)` |
| role\_id | UUID | Foreign key to `role(id)`     |

**Primary key:** (`user_id`, `role_id`)

### View: `user_company_roles_permissions`

Provides a complete list of users, their companies, roles, and permissions, including optional relationships.

### View: `user_company_roles_permissions_filtered`

Provides a strict list of users with fully assigned roles and permissions.

---

**Note:**

* All tables use UUID as the primary key.
* Timestamps default to the current server time using `CURRENT_TIMESTAMP`.
* Foreign keys use `ON DELETE CASCADE` or `ON DELETE SET NULL` appropriately.

This contract serves as the base structure to understand the entities and relationships managed within the authentication system.
