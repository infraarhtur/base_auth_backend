-- DROP SCHEMA public;

-- Crear el esquema público (sin autorización específica)
-- CREATE SCHEMA public AUTHORIZATION arhtur;

COMMENT ON SCHEMA public IS 'standard public schema';
-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.app_user definition

-- Drop table

-- DROP TABLE public.app_user;

CREATE TABLE public.app_user (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" text NOT NULL,
	email text NOT NULL,
	hashed_password text NOT NULL,
	is_active bool DEFAULT true NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_verified bool DEFAULT false NOT NULL,
	CONSTRAINT app_user_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_app_user_email ON public.app_user USING btree (email);
CREATE INDEX ix_app_user_id ON public.app_user USING btree (id);


-- public.company definition

-- Drop table

-- DROP TABLE public.company;

CREATE TABLE public.company (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" text NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	is_active bool DEFAULT true NOT NULL,
	CONSTRAINT company_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_company_id ON public.company USING btree (id);
CREATE INDEX ix_company_name ON public.company USING btree (name);


-- public."permission" definition

-- Drop table

-- DROP TABLE public."permission";

CREATE TABLE public."permission" (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" text NOT NULL,
    is_super_admin boolean NOT NULL DEFAULT false,
	CONSTRAINT permission_pkey PRIMARY KEY (id),
	CONSTRAINT uq_permission_name UNIQUE (name)
);
CREATE INDEX ix_permission_id ON public.permission USING btree (id);
CREATE INDEX ix_permission_name ON public.permission USING btree (name);


-- public.company_user definition

-- Drop table

-- DROP TABLE public.company_user;

CREATE TABLE public.company_user (
	company_id uuid NOT NULL,
	user_id uuid NOT NULL,
	is_active bool DEFAULT true NOT NULL,
	is_verified bool DEFAULT false NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT company_user_pkey PRIMARY KEY (company_id, user_id),
	CONSTRAINT company_user_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id) ON DELETE CASCADE,
	CONSTRAINT company_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(id) ON DELETE CASCADE
);
CREATE INDEX ix_company_user_company_id ON public.company_user USING btree (company_id);
CREATE INDEX ix_company_user_user_id ON public.company_user USING btree (user_id);


-- public.invalidated_tokens definition

-- Drop table

-- DROP TABLE public.invalidated_tokens;

CREATE TABLE public.invalidated_tokens (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	token_hash varchar(255) NOT NULL,
	user_id uuid NOT NULL,
	company_id uuid NULL,
	invalidated_at timestamptz DEFAULT now() NOT NULL,
	expires_at timestamptz NOT NULL,
	token_type varchar(20) NOT NULL,
	CONSTRAINT pk_invalidated_tokens PRIMARY KEY (id),
	CONSTRAINT fk_invalidated_tokens_company_id_company FOREIGN KEY (company_id) REFERENCES public.company(id),
	CONSTRAINT fk_invalidated_tokens_user_id_app_user FOREIGN KEY (user_id) REFERENCES public.app_user(id)
);
CREATE INDEX ix_invalidated_tokens_company_id ON public.invalidated_tokens USING btree (company_id);
CREATE INDEX ix_invalidated_tokens_expires_at ON public.invalidated_tokens USING btree (expires_at);
CREATE UNIQUE INDEX ix_invalidated_tokens_token_hash ON public.invalidated_tokens USING btree (token_hash);
CREATE INDEX ix_invalidated_tokens_user_id ON public.invalidated_tokens USING btree (user_id);


-- public."role" definition

-- Drop table

-- DROP TABLE public."role";

CREATE TABLE public."role" (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	company_id uuid NULL,
	"name" text NOT NULL,
	CONSTRAINT role_pkey PRIMARY KEY (id),
	CONSTRAINT role_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id) ON DELETE CASCADE
);
CREATE INDEX ix_role_company_id ON public.role USING btree (company_id);
CREATE INDEX ix_role_id ON public.role USING btree (id);
CREATE INDEX ix_role_name ON public.role USING btree (name);


-- public.role_permission definition

-- Drop table

-- DROP TABLE public.role_permission;

CREATE TABLE public.role_permission (
	role_id uuid NOT NULL,
	permission_id uuid NOT NULL,
	CONSTRAINT role_permission_pkey PRIMARY KEY (role_id, permission_id),
	CONSTRAINT role_permission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public."permission"(id) ON DELETE CASCADE,
	CONSTRAINT role_permission_role_id_fkey FOREIGN KEY (role_id) REFERENCES public."role"(id) ON DELETE CASCADE
);
CREATE INDEX ix_role_permission_permission_id ON public.role_permission USING btree (permission_id);
CREATE INDEX ix_role_permission_role_id ON public.role_permission USING btree (role_id);


-- public.user_identity definition

-- Drop table

-- DROP TABLE public.user_identity;

CREATE TABLE public.user_identity (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	user_id uuid NOT NULL,
	provider text NOT NULL,
	provider_user_id text NOT NULL,
	email text NULL,
	"name" text NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT user_identity_pkey PRIMARY KEY (id),
	CONSTRAINT user_identity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(id) ON DELETE CASCADE
);
CREATE INDEX ix_user_identity_id ON public.user_identity USING btree (id);
CREATE INDEX ix_user_identity_provider ON public.user_identity USING btree (provider);
CREATE INDEX ix_user_identity_provider_user_id ON public.user_identity USING btree (provider_user_id);
CREATE INDEX ix_user_identity_user_id ON public.user_identity USING btree (user_id);


-- public.user_role definition

-- Drop table

-- DROP TABLE public.user_role;

CREATE TABLE public.user_role (
	user_id uuid NOT NULL,
	role_id uuid NOT NULL,
	CONSTRAINT user_role_pkey PRIMARY KEY (user_id, role_id),
	CONSTRAINT user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public."role"(id) ON DELETE CASCADE,
	CONSTRAINT user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.app_user(id) ON DELETE CASCADE
);
CREATE INDEX ix_user_role_role_id ON public.user_role USING btree (role_id);
CREATE INDEX ix_user_role_user_id ON public.user_role USING btree (user_id);


-- public.user_company_roles_permissions source

CREATE OR REPLACE VIEW public.user_company_roles_permissions
AS SELECT cu.company_id,
    c.name AS company_name,
    u.id AS user_id,
    u.name AS user_name,
    u.email,
    r.id AS role_id,
    r.name AS role_name,
    p.id AS permission_id,
    p.name AS permission_name
   FROM company_user cu
     JOIN company c ON c.id = cu.company_id
     JOIN app_user u ON u.id = cu.user_id
     LEFT JOIN user_role ur ON ur.user_id = u.id
     LEFT JOIN role r ON r.id = ur.role_id AND r.company_id = cu.company_id
     LEFT JOIN role_permission rp ON rp.role_id = r.id
     LEFT JOIN permission p ON p.id = rp.permission_id;


-- public.user_company_roles_permissions_filtered source

CREATE OR REPLACE VIEW public.user_company_roles_permissions_filtered
AS SELECT cu.company_id,
    c.name AS company_name,
    u.id AS user_id,
    u.name AS user_name,
    u.email,
    r.id AS role_id,
    r.name AS role_name,
    p.id AS permission_id,
    p.name AS permission_name
   FROM company_user cu
     JOIN company c ON c.id = cu.company_id
     JOIN app_user u ON u.id = cu.user_id
     JOIN user_role ur ON ur.user_id = u.id
     JOIN role r ON r.id = ur.role_id AND r.company_id = cu.company_id
     JOIN role_permission rp ON rp.role_id = r.id
     JOIN permission p ON p.id = rp.permission_id;



	--DROP FUNCTION public.create_company_with_user(text, text, text);
-- Stored Procedure para crear una empresa con un usuario
-- Crea un rol admin relacionado a la empresa y le asigna todos los permisos disponibles

CREATE OR REPLACE FUNCTION create_company_with_user(
    p_company_name TEXT,
    p_user_name TEXT,
    p_user_email TEXT
)
RETURNS TABLE(
    out_company_id UUID,
    out_user_id UUID,
    out_admin_role_id UUID
) AS $$
DECLARE
    v_company_id UUID;
    v_user_id UUID;
    v_admin_role_id UUID;
    v_default_password TEXT := '$2b$12$TvsnnETjWySbme734iV00u7YmZul14Af1.crhsJXoq9OrXvVWOnXa';
    v_permission_record RECORD;
BEGIN
    -- Verificar que el email no existe
    IF EXISTS (SELECT 1 FROM app_user WHERE email = p_user_email) THEN
        RAISE EXCEPTION 'El email % ya está registrado', p_user_email;
    END IF;

    -- Verificar que no exista una empresa con el mismo nombre
    IF EXISTS (SELECT 1 FROM company WHERE "name" = p_company_name) THEN
        RAISE EXCEPTION 'Ya existe una empresa con el nombre %', p_company_name;
    END IF;

    -- Crear la empresa
    INSERT INTO company ("name", is_active, created_at)
    VALUES (p_company_name, true, CURRENT_TIMESTAMP)
    RETURNING id INTO v_company_id;

    -- Crear el usuario
    INSERT INTO app_user ("name", email, hashed_password, is_active, is_verified, created_at)
    VALUES (p_user_name, p_user_email, v_default_password, true, false, CURRENT_TIMESTAMP)
    RETURNING id INTO v_user_id;

    -- Relacionar el nuevo usuario con la nueva empresa
    INSERT INTO company_user (company_id, user_id, is_active, is_verified, created_at)
    VALUES (v_company_id, v_user_id, true, false, CURRENT_TIMESTAMP);

    -- Crear el rol admin para la nueva empresa (relacionado al company_id)
    INSERT INTO "role" (company_id, "name")
    VALUES (v_company_id, 'admin')
    RETURNING id INTO v_admin_role_id;

    -- Relacionar el rol admin a TODOS los permisos
    -- excepto los que contengan 'company:' en el campo name
    FOR v_permission_record IN
        SELECT id AS permission_id
        FROM "permission"
        WHERE name NOT LIKE '%company:%'
    LOOP
        INSERT INTO role_permission (role_id, permission_id)
        VALUES (v_admin_role_id, v_permission_record.permission_id)
        ON CONFLICT (role_id, permission_id) DO NOTHING;
    END LOOP;

    -- Asignar el rol admin al nuevo usuario
    INSERT INTO user_role (user_id, role_id)
    VALUES (v_user_id, v_admin_role_id)
    ON CONFLICT (user_id, role_id) DO NOTHING;

    -- Retornar los IDs creados
    RETURN QUERY
        SELECT
            v_company_id    AS out_company_id,
            v_user_id       AS out_user_id,
            v_admin_role_id AS out_admin_role_id;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso:
--SELECT * FROM create_company_with_user('Mi Empresa de prueba', 'Usuario prueba inventario', 'usuario.inventario@yopmail.com');
