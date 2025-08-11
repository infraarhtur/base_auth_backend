INSERT INTO public.app_user (id,"name",email,hashed_password,is_active,created_at,is_verified) VALUES
	 ('10000000-0000-0000-0000-000000000002'::uuid,'Bob Johnson','bob@biz.com','hashed_pw_2',true,'2025-07-30 17:53:31.574559-05',false),
	 ('10000000-0000-0000-0000-000000000003'::uuid,'Charlie Admin','charlie@both.com','$2b$12$WUGJERnKC0VMPgy9o/Z1E.OZpc6PqT6Z1bmXnwdsuwnWQZPePP7Sy',true,'2025-07-30 17:53:31.574559-05',false),
	 ('4a0f18b3-0c4b-41f8-95c4-ce0e288c8003'::uuid,'prueba TechCorp actualizada','user@example.com','$2b$12$YLvqjIKo3S0qojdi8GTC0.1bTxyRk7DXQJRsXb5u3skpGWNkMEFHW',true,'2025-08-08 15:36:12.366454-05',false),
	 ('b2c777ed-4b52-4fa2-9959-7a61524252e4'::uuid,'una prueba bien tesa','user3@example.com','$2b$12$wWvJzY.nzp.Ci5zxO0z90uo0lRWHvarFv59ywqSwmnHRFFKaaDIim',true,'2025-08-08 17:57:17.434789-05',false),
	 ('d3e5b31d-9c28-4d04-b584-4695d8711bd9'::uuid,'Usuario Test Cascade','test.cascade@example.com','hashed_password_test',true,'2025-08-09 18:15:08.080347-05',false),
	 ('10000000-0000-0000-0000-000000000001'::uuid,'Alice Smith','infraarhtur@outlook.com','$2b$12$Dpq2qaJmsMWnBEVKWbaZs.GFHxDTer15IczQI4S26XmcM2RkDTeoy',true,'2025-07-30 17:53:31.574559-05',true);


INSERT INTO public.company (id,"name",created_at,is_active) VALUES
	 ('00000000-0000-0000-0000-000000000001'::uuid,'TechCorp','2025-07-30 17:53:31.574559-05',true),
	 ('00000000-0000-0000-0000-000000000002'::uuid,'BizSolutions','2025-07-30 17:53:31.574559-05',true),
	 ('a74785ec-e4cc-4ffa-a507-e656dd5c8119'::uuid,'Empresa de prueba','2025-08-08 18:07:40.312621-05',true),
	 ('66b017c1-5ad3-4acb-8246-8d1b9582a299'::uuid,'Empresa de prueba 2','2025-08-08 18:11:50.94642-05',true),
	 ('eff47089-a7f2-4016-9237-4e4e4753510e'::uuid,'Empresa de prueba 3','2025-08-08 18:19:37.557313-05',true),
	 ('d81b2457-d0c8-4c0d-b957-00a985919963'::uuid,'Empresa de prueba 5','2025-08-08 18:24:33.747502-05',true),
	 ('ccb78dca-4586-4ce5-8cb6-187a2dbefc2e'::uuid,'Empresa de prueba 6','2025-08-08 18:25:24.198482-05',true),
	 ('2d644cfd-8652-483a-9b29-49a00cb126ca'::uuid,'Empresa de prueba 7','2025-08-08 18:29:13.405103-05',true),
	 ('90b7c311-58f1-49ba-a255-cc37027c5418'::uuid,'Empresa de prueba 10','2025-08-08 19:05:00.145247-05',true),
	 ('1f4f7ee3-dff1-41ea-9cd8-5283e69de5d0'::uuid,'Empresa de prueba 8','2025-08-08 18:32:38.28189-05',false);

INSERT INTO public.company (id,"name",created_at,is_active) VALUES
	 ('e2ab239d-101e-4a1b-9f3f-3ebb8c9bab4a'::uuid,'Empresa Test Cascade','2025-08-09 18:14:47.95624-05',true),
	 ('d2fe777f-006e-4d37-ac62-5e6e4976ff4c'::uuid,'Empresa Test Cascade','2025-08-09 18:15:08.070455-05',true);

INSERT INTO public.company_user (company_id,user_id,is_active,created_at) VALUES
	 ('00000000-0000-0000-0000-000000000001'::uuid,'10000000-0000-0000-0000-000000000001'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('00000000-0000-0000-0000-000000000002'::uuid,'10000000-0000-0000-0000-000000000002'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('00000000-0000-0000-0000-000000000001'::uuid,'10000000-0000-0000-0000-000000000003'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('00000000-0000-0000-0000-000000000002'::uuid,'10000000-0000-0000-0000-000000000003'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('00000000-0000-0000-0000-000000000001'::uuid,'4a0f18b3-0c4b-41f8-95c4-ce0e288c8003'::uuid,false,'2025-08-09 13:48:25.96452-05'),
	 ('a74785ec-e4cc-4ffa-a507-e656dd5c8119'::uuid,'10000000-0000-0000-0000-000000000003'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('66b017c1-5ad3-4acb-8246-8d1b9582a299'::uuid,'10000000-0000-0000-0000-000000000003'::uuid,true,'2025-08-09 13:48:25.96452-05'),
	 ('00000000-0000-0000-0000-000000000001'::uuid,'b2c777ed-4b52-4fa2-9959-7a61524252e4'::uuid,false,'2025-08-09 13:48:25.96452-05'),
	 ('a74785ec-e4cc-4ffa-a507-e656dd5c8119'::uuid,'4a0f18b3-0c4b-41f8-95c4-ce0e288c8003'::uuid,false,'2025-08-09 13:48:25.96452-05');


INSERT INTO public."permission" (id,"name") VALUES
	 ('30000000-0000-0000-0000-000000000001'::uuid,'create_users'),
	 ('30000000-0000-0000-0000-000000000002'::uuid,'view_reports'),
	 ('30000000-0000-0000-0000-000000000003'::uuid,'manage_roles'),
	 ('fea3ba35-4489-4fc3-9037-504ea5afa841'::uuid,'user:read'),
	 ('320feefe-7467-43e0-83bd-8f5f5c6651bf'::uuid,'user:create'),
	 ('1a7ed8b8-aef8-428b-a39b-c9a3678399e7'::uuid,'user:update'),
	 ('a6dc66a2-126e-48ef-a1db-7c9ad6ae0649'::uuid,'user:delete'),
	 ('77f8c2c8-0782-4c1f-bc27-740936cf098f'::uuid,'company:read'),
	 ('4772c37a-0797-419d-a154-d618b9b15c8f'::uuid,'company:create'),
	 ('864dfcb3-0979-4af4-99de-f14464c784f4'::uuid,'company:update');
INSERT INTO public."permission" (id,"name") VALUES
	 ('43923e81-1b47-4546-9ac5-2f6cb0972403'::uuid,'company:delete'),
	 ('41592a05-8afd-453d-a3c2-309661719efa'::uuid,'role:read'),
	 ('cee14831-0929-4b56-9411-4d9abe192505'::uuid,'role:create'),
	 ('4179213f-a434-4b6f-9a80-18e9bfb68569'::uuid,'role:update'),
	 ('92e93b7d-3c81-4527-b2ec-adc337c716b2'::uuid,'role:delete'),
	 ('83da9238-2acc-4b0c-bb08-082bfc436cb4'::uuid,'permission:read'),
	 ('3542e07d-c5b8-4360-a52d-86b518644d58'::uuid,'permission:assign'),
	 ('ad85e94f-02d1-4d23-9d01-d5d16d07da0c'::uuid,'system:admin'),
	 ('ca4d2439-8e33-4b2e-aabd-555825f3ec92'::uuid,'dashboard:read'),
	 ('b553e5f3-da30-4daa-9f24-f3b832913102'::uuid,'reports:read');
INSERT INTO public."permission" (id,"name") VALUES
	 ('e738ba99-b6b7-44e5-8bac-697389b3415a'::uuid,'settings:read'),
	 ('3e80c34a-c365-40dd-9569-3f3a4394da53'::uuid,'settings:update');


INSERT INTO public."role" (id,company_id,"name") VALUES
	 ('20000000-0000-0000-0000-000000000001'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Admin'),
	 ('20000000-0000-0000-0000-000000000002'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'User'),
	 ('20000000-0000-0000-0000-000000000003'::uuid,'00000000-0000-0000-0000-000000000002'::uuid,'Manager'),
	 ('20000000-0000-0000-0000-000000000004'::uuid,'00000000-0000-0000-0000-000000000002'::uuid,'User'),
	 ('3d8acef0-bf5a-4139-b159-e6e4fdbccafd'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Cashier_1'),
	 ('06029467-6ab5-4045-a05b-674dd2ef9ad7'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Cashier_2'),
	 ('ba52d1c3-551e-49e0-82dc-6d211aea0e07'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Cashier_3'),
	 ('19ee7808-9a21-4a2e-809e-23e634ac1229'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Cashier_4'),
	 ('285aed59-60ee-41c8-b770-679eee86ec9c'::uuid,'00000000-0000-0000-0000-000000000001'::uuid,'Cashier_5');

INSERT INTO public.role_permission (role_id,permission_id) VALUES
	 ('20000000-0000-0000-0000-000000000002'::uuid,'30000000-0000-0000-0000-000000000002'::uuid),
	 ('20000000-0000-0000-0000-000000000003'::uuid,'30000000-0000-0000-0000-000000000002'::uuid),
	 ('20000000-0000-0000-0000-000000000004'::uuid,'30000000-0000-0000-0000-000000000002'::uuid),
	 ('3d8acef0-bf5a-4139-b159-e6e4fdbccafd'::uuid,'fea3ba35-4489-4fc3-9037-504ea5afa841'::uuid),
	 ('3d8acef0-bf5a-4139-b159-e6e4fdbccafd'::uuid,'320feefe-7467-43e0-83bd-8f5f5c6651bf'::uuid),
	 ('3d8acef0-bf5a-4139-b159-e6e4fdbccafd'::uuid,'1a7ed8b8-aef8-428b-a39b-c9a3678399e7'::uuid),
	 ('06029467-6ab5-4045-a05b-674dd2ef9ad7'::uuid,'fea3ba35-4489-4fc3-9037-504ea5afa841'::uuid),
	 ('06029467-6ab5-4045-a05b-674dd2ef9ad7'::uuid,'320feefe-7467-43e0-83bd-8f5f5c6651bf'::uuid),
	 ('06029467-6ab5-4045-a05b-674dd2ef9ad7'::uuid,'1a7ed8b8-aef8-428b-a39b-c9a3678399e7'::uuid),
	 ('ba52d1c3-551e-49e0-82dc-6d211aea0e07'::uuid,'fea3ba35-4489-4fc3-9037-504ea5afa841'::uuid);
INSERT INTO public.role_permission (role_id,permission_id) VALUES
	 ('ba52d1c3-551e-49e0-82dc-6d211aea0e07'::uuid,'320feefe-7467-43e0-83bd-8f5f5c6651bf'::uuid),
	 ('ba52d1c3-551e-49e0-82dc-6d211aea0e07'::uuid,'1a7ed8b8-aef8-428b-a39b-c9a3678399e7'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'a6dc66a2-126e-48ef-a1db-7c9ad6ae0649'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'30000000-0000-0000-0000-000000000001'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'30000000-0000-0000-0000-000000000002'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'30000000-0000-0000-0000-000000000003'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'fea3ba35-4489-4fc3-9037-504ea5afa841'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'320feefe-7467-43e0-83bd-8f5f5c6651bf'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'1a7ed8b8-aef8-428b-a39b-c9a3678399e7'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'77f8c2c8-0782-4c1f-bc27-740936cf098f'::uuid);
INSERT INTO public.role_permission (role_id,permission_id) VALUES
	 ('20000000-0000-0000-0000-000000000001'::uuid,'4772c37a-0797-419d-a154-d618b9b15c8f'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'864dfcb3-0979-4af4-99de-f14464c784f4'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'43923e81-1b47-4546-9ac5-2f6cb0972403'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'41592a05-8afd-453d-a3c2-309661719efa'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'cee14831-0929-4b56-9411-4d9abe192505'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'4179213f-a434-4b6f-9a80-18e9bfb68569'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'92e93b7d-3c81-4527-b2ec-adc337c716b2'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'83da9238-2acc-4b0c-bb08-082bfc436cb4'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'3542e07d-c5b8-4360-a52d-86b518644d58'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'ad85e94f-02d1-4d23-9d01-d5d16d07da0c'::uuid);
INSERT INTO public.role_permission (role_id,permission_id) VALUES
	 ('20000000-0000-0000-0000-000000000001'::uuid,'ca4d2439-8e33-4b2e-aabd-555825f3ec92'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'b553e5f3-da30-4daa-9f24-f3b832913102'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'e738ba99-b6b7-44e5-8bac-697389b3415a'::uuid),
	 ('20000000-0000-0000-0000-000000000001'::uuid,'3e80c34a-c365-40dd-9569-3f3a4394da53'::uuid);

INSERT INTO public.user_role (user_id,role_id) VALUES
	 ('10000000-0000-0000-0000-000000000001'::uuid,'20000000-0000-0000-0000-000000000002'::uuid),
	 ('10000000-0000-0000-0000-000000000003'::uuid,'20000000-0000-0000-0000-000000000001'::uuid),
	 ('10000000-0000-0000-0000-000000000002'::uuid,'20000000-0000-0000-0000-000000000003'::uuid),
	 ('10000000-0000-0000-0000-000000000003'::uuid,'20000000-0000-0000-0000-000000000004'::uuid),
	 ('4a0f18b3-0c4b-41f8-95c4-ce0e288c8003'::uuid,'20000000-0000-0000-0000-000000000002'::uuid),
	 ('b2c777ed-4b52-4fa2-9959-7a61524252e4'::uuid,'20000000-0000-0000-0000-000000000002'::uuid);
