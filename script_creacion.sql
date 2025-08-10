BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 66c32d7a84dd

INSERT INTO alembic_version (version_num) VALUES ('66c32d7a84dd') RETURNING alembic_version.version_num;

-- Running upgrade 66c32d7a84dd -> 6b732f6dabcf

UPDATE alembic_version SET version_num='6b732f6dabcf' WHERE alembic_version.version_num = '66c32d7a84dd';

-- Running upgrade 6b732f6dabcf -> 31b015770dbc

UPDATE alembic_version SET version_num='31b015770dbc' WHERE alembic_version.version_num = '6b732f6dabcf';

-- Running upgrade 31b015770dbc -> 177d058d549e

UPDATE alembic_version SET version_num='177d058d549e' WHERE alembic_version.version_num = '31b015770dbc';

-- Running upgrade 177d058d549e -> 28186d2b3882

ALTER TABLE app_user ADD COLUMN username VARCHAR(100) NOT NULL;

ALTER TABLE app_user ADD COLUMN first_name VARCHAR(100) NOT NULL;

ALTER TABLE app_user ADD COLUMN last_name VARCHAR(100) NOT NULL;

ALTER TABLE app_user ADD COLUMN is_superuser BOOLEAN NOT NULL;

ALTER TABLE app_user ADD COLUMN is_verified BOOLEAN NOT NULL;

ALTER TABLE app_user ADD COLUMN phone VARCHAR(20);

ALTER TABLE app_user ADD COLUMN avatar_url VARCHAR(500);

ALTER TABLE app_user ADD COLUMN preferences TEXT;

ALTER TABLE app_user ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE app_user ALTER COLUMN email TYPE VARCHAR(255);

ALTER TABLE app_user ALTER COLUMN hashed_password TYPE VARCHAR(255);

ALTER TABLE app_user ALTER COLUMN is_active SET NOT NULL;

ALTER TABLE app_user ALTER COLUMN id TYPE INTEGER;

ALTER TABLE app_user ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE;

ALTER TABLE app_user ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE app_user DROP CONSTRAINT app_user_email_key;

CREATE INDEX ix_app_user_active ON app_user (is_active);

CREATE UNIQUE INDEX ix_app_user_email ON app_user (email);

CREATE INDEX ix_app_user_id ON app_user (id);

CREATE INDEX ix_app_user_superuser ON app_user (is_superuser);

CREATE UNIQUE INDEX ix_app_user_username ON app_user (username);

ALTER TABLE app_user DROP COLUMN name;

ALTER TABLE company ADD COLUMN description TEXT;

ALTER TABLE company ADD COLUMN domain VARCHAR(255);

ALTER TABLE company ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE company ADD COLUMN settings TEXT;

ALTER TABLE company ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE company ALTER COLUMN name TYPE VARCHAR(255);

ALTER TABLE company ALTER COLUMN id TYPE INTEGER;

ALTER TABLE company ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE;

ALTER TABLE company ALTER COLUMN created_at SET NOT NULL;

CREATE INDEX ix_company_active ON company (is_active);

CREATE INDEX ix_company_domain ON company (domain);

CREATE INDEX ix_company_id ON company (id);

CREATE INDEX ix_company_name ON company (name);

ALTER TABLE company ADD CONSTRAINT uq_company_domain UNIQUE (domain);

ALTER TABLE company_user ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE company_user ADD COLUMN joined_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE company_user ADD COLUMN id INTEGER NOT NULL;

ALTER TABLE company_user ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE company_user ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE company_user ALTER COLUMN user_id TYPE INTEGER;

ALTER TABLE company_user ALTER COLUMN company_id TYPE INTEGER;

CREATE INDEX ix_company_user_active ON company_user (is_active);

CREATE INDEX ix_company_user_company_id ON company_user (company_id);

CREATE INDEX ix_company_user_id ON company_user (id);

CREATE UNIQUE INDEX ix_company_user_unique ON company_user (user_id, company_id);

CREATE INDEX ix_company_user_user_id ON company_user (user_id);

ALTER TABLE permission ADD COLUMN description TEXT;

ALTER TABLE permission ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE permission ADD COLUMN is_system BOOLEAN NOT NULL;

ALTER TABLE permission ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE permission ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE permission ALTER COLUMN name TYPE VARCHAR(100);

ALTER TABLE permission ALTER COLUMN id TYPE INTEGER;

ALTER TABLE permission DROP CONSTRAINT permission_name_key;

CREATE INDEX ix_permission_active ON permission (is_active);

CREATE INDEX ix_permission_id ON permission (id);

CREATE UNIQUE INDEX ix_permission_name ON permission (name);

CREATE INDEX ix_permission_system ON permission (is_system);

ALTER TABLE role ADD COLUMN description TEXT;

ALTER TABLE role ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE role ADD COLUMN is_system BOOLEAN NOT NULL;

ALTER TABLE role ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE role ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE role ALTER COLUMN name TYPE VARCHAR(100);

ALTER TABLE role ALTER COLUMN company_id TYPE INTEGER;

ALTER TABLE role ALTER COLUMN id TYPE INTEGER;

ALTER TABLE role DROP CONSTRAINT role_company_id_name_key;

CREATE INDEX ix_role_active ON role (is_active);

CREATE INDEX ix_role_company_id ON role (company_id);

CREATE INDEX ix_role_id ON role (id);

CREATE INDEX ix_role_name ON role (name);

CREATE INDEX ix_role_system ON role (is_system);

ALTER TABLE role_permission ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE role_permission ADD COLUMN assigned_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE role_permission ADD COLUMN id INTEGER NOT NULL;

ALTER TABLE role_permission ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE role_permission ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE role_permission ALTER COLUMN role_id TYPE INTEGER;

ALTER TABLE role_permission ALTER COLUMN permission_id TYPE INTEGER;

CREATE INDEX ix_role_permission_active ON role_permission (is_active);

CREATE INDEX ix_role_permission_id ON role_permission (id);

CREATE INDEX ix_role_permission_permission_id ON role_permission (permission_id);

CREATE INDEX ix_role_permission_role_id ON role_permission (role_id);

CREATE UNIQUE INDEX ix_role_permission_unique ON role_permission (role_id, permission_id);

ALTER TABLE user_identity ADD COLUMN provider_email VARCHAR(255);

ALTER TABLE user_identity ADD COLUMN provider_name VARCHAR(255);

ALTER TABLE user_identity ADD COLUMN provider_avatar VARCHAR(500);

ALTER TABLE user_identity ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE user_identity ADD COLUMN is_verified BOOLEAN NOT NULL;

ALTER TABLE user_identity ADD COLUMN provider_data TEXT;

ALTER TABLE user_identity ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE user_identity ALTER COLUMN user_id TYPE INTEGER;

ALTER TABLE user_identity ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE user_identity ALTER COLUMN provider TYPE VARCHAR(50);

ALTER TABLE user_identity ALTER COLUMN provider_user_id TYPE VARCHAR(255);

ALTER TABLE user_identity ALTER COLUMN id TYPE INTEGER;

ALTER TABLE user_identity ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE;

ALTER TABLE user_identity ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE user_identity DROP CONSTRAINT user_identity_provider_provider_user_id_key;

CREATE INDEX ix_user_identity_active ON user_identity (is_active);

CREATE INDEX ix_user_identity_id ON user_identity (id);

CREATE INDEX ix_user_identity_provider ON user_identity (provider);

CREATE INDEX ix_user_identity_provider_user_id ON user_identity (provider_user_id);

CREATE UNIQUE INDEX ix_user_identity_unique ON user_identity (provider, provider_user_id);

CREATE INDEX ix_user_identity_user_id ON user_identity (user_id);

ALTER TABLE user_identity DROP COLUMN name;

ALTER TABLE user_identity DROP COLUMN email;

ALTER TABLE user_role ADD COLUMN is_active BOOLEAN NOT NULL;

ALTER TABLE user_role ADD COLUMN assigned_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE user_role ADD COLUMN id INTEGER NOT NULL;

ALTER TABLE user_role ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE user_role ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE user_role ALTER COLUMN user_id TYPE INTEGER;

ALTER TABLE user_role ALTER COLUMN role_id TYPE INTEGER;

CREATE INDEX ix_user_role_active ON user_role (is_active);

CREATE INDEX ix_user_role_id ON user_role (id);

CREATE INDEX ix_user_role_role_id ON user_role (role_id);

CREATE UNIQUE INDEX ix_user_role_unique ON user_role (user_id, role_id);

CREATE INDEX ix_user_role_user_id ON user_role (user_id);

UPDATE alembic_version SET version_num='28186d2b3882' WHERE alembic_version.version_num = '177d058d549e';

COMMIT;

