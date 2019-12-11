-- To impliment ltree
-- https://coderwall.com/p/whf3-a/hierarchical-data-in-postgres
CREATE EXTENSION ltree;
!!!
ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl" DROP COLUMN ltree_path;
!!!
ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl" ADD COLUMN ltree_path ltree;
!!!
CREATE INDEX parent_id_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" USING GIST (ltree_path);
!!!
CREATE INDEX parent_path_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" (parent_id_id);
!!!
ALTER TABLE public."djangoAPI_AvantisAdditions" DROP COLUMN full_path;
!!!
ALTER TABLE public."djangoAPI_AvantisAdditions" ADD COLUMN full_path ltree;
!!!
CREATE INDEX aa_parent_id_idx ON public."djangoAPI_AvantisAdditions" USING GIST (full_path);
!!!
CREATE INDEX aa_parent_path_idx ON public."djangoAPI_AvantisAdditions" (parent_mtoi_id);
!!!
CREATE OR REPLACE FUNCTION update_parent_path() RETURNS TRIGGER AS $$
    DECLARE
        path ltree;
    BEGIN
        IF NEW.parent_id_id IS NULL THEN
            NEW.ltree_path = ((new.id::text)::ltree);
        ELSEIF TG_OP = 'INSERT' OR OLD.parent_id_id IS NULL OR OLD.parent_id_id != NEW.parent_id_id THEN
            SELECT ltree_path FROM public."djangoAPI_ProjectAssetRoleRecordTbl" WHERE id = NEW.parent_id_id INTO path;
            IF path IS NULL THEN
                RAISE EXCEPTION 'Invalid parent_id %. Entities must be added parents first', NEW.parent_id_id;
            END IF;
            path = path || new.id::text;
            NEW.ltree_path = path;
            UPDATE public."djangoAPI_ProjectAssetRoleRecordTbl"
                SET ltree_path = path || subpath(ltree_path,nlevel(OLD.ltree_path)) WHERE ltree_path <@ OLD.ltree_path and ltree_path != old.ltree_path;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
!!!
CREATE TRIGGER parent_path_tgr
    BEFORE INSERT OR UPDATE ON public."djangoAPI_ProjectAssetRoleRecordTbl"
    FOR EACH ROW EXECUTE PROCEDURE update_parent_path();
!!!
CREATE OR REPLACE FUNCTION update_avantis_additions() RETURNS TRIGGER AS $$
    DECLARE
        ltree_path ltree;
        old_path ltree;
        parent_mtoi int;
        role_number_pk int;
    BEGIN
        select mtoi from public."djangoAPI_ClonedAssetAndRoleInRegistryTbl" where role_number = new.parent_role_number into parent_mtoi;
        select id from public."djangoAPI_MasterRoleNumbersTbl" where role_number = new.role_number into role_number_pk;
        IF NEW.parent_role_number = '' then
            raise notice 'parent role number is empty';
            ltree_path = ((new.mtoi::text)::ltree);
        else
            raise notice 'parent role number is NOT empty';
            SELECT full_path FROM public."djangoAPI_AvantisAdditions" WHERE clonedassetandroleinregistrytbl_ptr_id = parent_mtoi INTO ltree_path;
            IF ltree_path IS NULL THEN
                RAISE EXCEPTION 'Invalid parent_id %. Entities must be added parents first', NEW.parent_role_number;
            END IF;
            ltree_path = ltree_path || new.mtoi::text;
            raise notice 'ltree_path is %', ltree_path;
        end if;
        if TG_OP = 'INSERT' then
            insert into public."djangoAPI_AvantisAdditions"(clonedassetandroleinregistrytbl_ptr_id, full_path, parent_mtoi_id, linked_role_number_id) values(new.mtoi, ltree_path, parent_mtoi, role_number_pk);
        elseif TG_OP = 'UPDATE' then 
            raise notice 'updating old values';
            select full_path from public."djangoAPI_AvantisAdditions" where clonedassetandroleinregistrytbl_ptr_id = new.mtoi into old_path;
            -- update the data for the coorsponding entry
            update public."djangoAPI_AvantisAdditions" 
                set full_path = ltree_path, parent_mtoi_id = parent_mtoi where clonedassetandroleinregistrytbl_ptr_id = new.mtoi;
            -- update path for all children
            UPDATE public."djangoAPI_AvantisAdditions"
                SET full_path = ltree_path || subpath(full_path,nlevel(old_path)) WHERE full_path <@ old_path and full_path != old_path;
            update public."djangoAPI_MasterRoleNumbersTbl"
                set role_number = new.role_number where id = role_number_pk;
        end if;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
!!!
CREATE TRIGGER avantis_additions_tgr
    BEFORE INSERT OR UPDATE ON public."djangoAPI_ClonedAssetAndRoleInRegistryTbl"
    FOR EACH ROW EXECUTE PROCEDURE update_avantis_additions();
!!!
create or replace
view reservation_view as
select
    mtoi as id,
    role_number,
    role_name,
    parent_mtoi_id as parent,
    project_tbl_id as project_id,
    full_path,
    approved,
    (not project_tbl_id is null) as reserved,
    (case
        when (approved) and (not project_tbl_id is null) then 'Approved'
        -- true + true
        when (not approved) and (not project_tbl_id is null) then 'Pending'
        -- false + true
    end ) as approval_status,
    (role_exists and asset_exists and (not parent_changed) and (not role_changed)) as reservable
from
    ((public."djangoAPI_ClonedAssetAndRoleInRegistryTbl" as c
left join public."djangoAPI_AvantisAdditions" as a on
    c.mtoi = a.clonedassetandroleinregistrytbl_ptr_id) as ca
left join ((select projectassetrolerecordtbl_ptr_id, entity_exists as role_exists, parent_changed, cloned_role_registry_tbl_id from public."djangoAPI_PreDesignReconciledRoleRecordTbl") as pa
left join (select id, approved, project_tbl_id from public."djangoAPI_ProjectAssetRoleRecordTbl") as ra on
    pa.projectassetrolerecordtbl_ptr_id = ra.id) as pr on
    ca.mtoi = pr.cloned_role_registry_tbl_id) as d
left join (select projectassetrecordtbl_ptr_id, entity_exists as asset_exists, role_changed, cloned_role_registry_tbl_id from public."djangoAPI_PreDesignReconciledAssetRecordTbl") as e on
    d.mtoi = e.cloned_role_registry_tbl_id;
!!!
CREATE OR REPLACE FUNCTION update_parent_changed() RETURNS TRIGGER AS $$
-- only run on updates, since insert implies that the entity did not exist in avantis to begin with, which means this does not apply (false)
    DECLARE
    new_parent_mtoi int;
    orig_parent_mtoi int;
    status bool;
    begin
--	    only run trigger if the entry is predesign
        if exists (select 1 from public."djangoAPI_PreDesignReconciledRoleRecordTbl" as rr1 where rr1.projectassetrolerecordtbl_ptr_id = new.id) then
            status = false;
            IF OLD.parent_id_id != NEW.parent_id_id then
                select
                    cloned_role_registry_tbl_id
                from
                    public."djangoAPI_PreDesignReconciledRoleRecordTbl"
                where
                    projectassetrolerecordtbl_ptr_id  = new.parent_id_id
                into
                    new_parent_mtoi;
                
                select
                    mtoi
                from
                    public."djangoAPI_ClonedAssetAndRoleInRegistryTbl"
                where
                    role_number = (
                    select
                        parent_role_number
                    from
                        public."djangoAPI_ClonedAssetAndRoleInRegistryTbl"
                    where
                        mtoi = (
                        select
                            cloned_role_registry_tbl_id
                        from
                            public."djangoAPI_PreDesignReconciledRoleRecordTbl"
                        where
                            projectassetrolerecordtbl_ptr_id = new.id))
                into
                    orig_parent_mtoi;
--				raise exception 'new mtoi %, old mtoi %', new_parent_mtoi, orig_parent_mtoi;
                if new_parent_mtoi <> orig_parent_mtoi then
                    status = true;
                end if;
            elsif OLD.parent_id_id = NEW.parent_id_id then -- if the parent didnt change just use the old one
                select parent_changed from public."djangoAPI_PreDesignReconciledRoleRecordTbl" as rr where rr.projectassetrolerecordtbl_ptr_id = new.id into status;
            END IF;
            update public."djangoAPI_PreDesignReconciledRoleRecordTbl" as rr set parent_changed = status where rr.projectassetrolerecordtbl_ptr_id = new.id;
        end if;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
!!!
CREATE TRIGGER parent_changed_tgr
    BEFORE insert or UPDATE ON public."djangoAPI_ProjectAssetRoleRecordTbl"
    FOR EACH ROW EXECUTE PROCEDURE update_parent_changed();
!!!
CREATE OR REPLACE FUNCTION update_role_changed() RETURNS TRIGGER AS $$
-- only run on updates, since insert implies that the entity did not exist in avantis to begin with, which means this does not apply (false)
    DECLARE
    new_role_mtoi int;
    orig_role_mtoi int;
    status bool;
    begin
--	    only run trigger if the entry is predesign
        status = false;
    --	raise exception 'new role %, old role %', NEW.initial_project_asset_role_id_id, OLD.initial_project_asset_role_id_id;
        IF OLD.initial_project_asset_role_id_id != NEW.initial_project_asset_role_id_id or OLD.initial_project_asset_role_id_id is null or NEW.initial_project_asset_role_id_id is null then
            new_role_mtoi = new.cloned_role_registry_tbl_id;
            select cloned_role_registry_tbl_id from public."djangoAPI_PreDesignReconciledRoleRecordTbl"  as rr where rr.projectassetrolerecordtbl_ptr_id = new.initial_project_asset_role_id_id into orig_role_mtoi;
    --     	raise exception 'new role %, old role %', new_role_mtoi, orig_role_mtoi;
        if new_role_mtoi <> orig_role_mtoi then
                status = true;
            end if;
        END IF;
        new.role_changed = status;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;
!!!
create trigger role_changed_tgr
    before insert or update on public."djangoAPI_PreDesignReconciledAssetRecordTbl"
    for each row execute procedure update_role_changed();
-- https://stackoverflow.com/questions/23257059/postgresql-exclude-records-crossing-other-table-values
-- probably should do this to exclude removed roles
!!!
create or replace
view pre_base_asset_view as
select
	id as asset_id,
	asset_serial_number,
	project_tbl_id as project_id,
	designer_planned_action_type_tbl_id,
	coalesce(role_changed, false) as role_changed,
	coalesce(parent_for_new, parent_after_move, initial_project_asset_role_id_id) as role_link,
	coalesce(move_installation_stage_id, new_installation_stage_id) as installation_stage_id,
	move_uninstallation_stage_id as uninstallation_stage_id,
	entity_exists as asset_exists,
	(not NewAsset.new_link is null) as asset_new,
    coalesce(missing_from_registry, false) as asset_missing_from_registry
from
	((public."djangoAPI_ProjectAssetRecordTbl" as BaseAsset
left join public."djangoAPI_PreDesignReconciledAssetRecordTbl" as PreAsset on
	BaseAsset.id = PreAsset.projectassetrecordtbl_ptr_id) as BasePreAsset
left join (
	select
		final_project_asset_role_id_id as parent_after_move,
		predesignreconciledassetrecordtbl_ptr_id as move_link,
		installation_stage_id as move_installation_stage_id,
		uninstallation_stage_id as move_uninstallation_stage_id
	from
		public."djangoAPI_ExistingAssetMovedByProjectTbl") as MovedAsset on
	BasePreAsset.id = MovedAsset.move_link) as BasePreMovedAsset
left join (
	select
		final_project_asset_role_id_id as parent_for_new,
		projectassetrecordtbl_ptr_id as new_link,
		installation_stage_id as new_installation_stage_id
	from
		public."djangoAPI_NewAssetDeliveredByProjectTbl") as NewAsset on
	BasePreMovedAsset.id = NewAsset.new_link
!!!
create or replace
view asset_moved_assigned as
select
predesignreconciledassetrecordtbl_ptr_id as id,
not (final_project_asset_role_id_id is null) as assigned
from public."djangoAPI_ExistingAssetMovedByProjectTbl"
!!!
create or replace
view base_asset_view as
select
asset_id,
asset_serial_number,
project_id,
designer_planned_action_type_tbl_id,
role_changed,
case assigned
	when false then null
	else role_link
end as role_link,
installation_stage_id,
uninstallation_stage_id,
asset_exists,
asset_new,
asset_missing_from_registry
from
pre_base_asset_view as ba
left join asset_moved_assigned as ma
on ba.asset_id = ma.id
!!!
create or replace
view reconciliation_unassigned_asset_view as
select
	asset_id as id,
	asset_serial_number,
	project_id,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	base_asset_view
where
	role_link is null
    and designer_planned_action_type_tbl_id <> 'b'
	and asset_new = false
	and asset_exists = true;
!!!
create or replace
view garbage_can_asset_view as
select
	asset_id as id,
	asset_serial_number,
	project_id,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	base_asset_view
where
	role_link is null
    and designer_planned_action_type_tbl_id <> 'b'
	and asset_new = false
	and asset_exists = false;
!!!
create or replace
view change_unassigned_asset_view as
select
	asset_id as id,
	asset_serial_number,
	project_id,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	base_asset_view
where
	role_link is null
    and designer_planned_action_type_tbl_id <> 'b'
	and asset_exists = true;
!!!
create or replace
view dumpster_asset_view as
select
	asset_id as id,
	asset_serial_number,
	project_id,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	base_asset_view
where
	role_link is null
    and designer_planned_action_type_tbl_id = 'b'
	and asset_exists = true;
!!!
create or replace
view base_role_view as
select
	id,
	role_name,
	role_number as role_number,
	parent_id_id as parent,
	project_tbl_id as project_id,
	coalesce(entity_exists, true) as role_exists,
	coalesce(missing_from_registry, false) as role_missing_from_registry,
	ltree_path as full_path,
	coalesce(parent_changed, false) as parent_changed,
	approved,
	coalesce(new_role, false) as role_new,
	coalesce(disposed, false) as role_disposed
from
	(((public."djangoAPI_ProjectAssetRoleRecordTbl" as BaseRole
left join public."djangoAPI_PreDesignReconciledRoleRecordTbl" as PreRole on
	BaseRole.id = PreRole.projectassetrolerecordtbl_ptr_id) as BasePreRole
left join (
	select
		new_role,
		projectassetrolerecordtbl_ptr_id as link
	from
		public."djangoAPI_NewProjectAssetRoleTbl") as NewRole on
	BasePreRole.id = NewRole.link) as Roles
left join (select id as idrn, role_number from public."djangoAPI_MasterRoleNumbersTbl") as RoleNum on
Roles.updatable_role_number_id = RoleNum.idrn) as RolesWNames
left join public."djangoAPI_ExistingRoleDisposedByProject" as DisposeRole on
	RolesWNames.id = DisposeRole.predesignreconciledrolerecordtbl_ptr_id
!!!
create or replace
view joined_role_asset as
select
	id,
	role_name,
	role_number,
	parent,
	base_role_view.project_id,
	role_exists,
	role_missing_from_registry,
	full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	coalesce(role_changed, false) as role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	coalesce(asset_exists, true) as asset_exists,
	coalesce(asset_new, false) as asset_new,
    coalesce(asset_missing_from_registry, false) as asset_missing_from_registry
from
	(base_role_view
left join base_asset_view on
	base_role_view.id = base_asset_view.role_link)
!!!
create or replace
view reconciliation_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, 1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
full_path <@ '1'::ltree and role_exists = true and role_disposed = false and role_new = false and full_path <> '1'::ltree;
!!!
create or replace
view reconciliation_orphan_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, 1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
full_path <@ '2'::ltree and role_exists = true and role_disposed = false and role_new = false and full_path <> '2'::ltree;
!!!
create or replace
view garbage_can_reconciliation_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, -1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
nlevel(full_path) > 1 and role_exists = false and role_disposed = false and role_new = false;
!!!
create or replace
view change_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, 1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
full_path <@ '1'::ltree and role_exists = true and role_disposed = false and full_path <> '1'::ltree;
!!!
create or replace
view change_orphan_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, 1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
full_path <@ '2'::ltree and role_exists = true and role_disposed = false and full_path <> '2'::ltree;
!!!
create or replace
view dumpster_change_view as
select
	id,
	role_name,
	role_number,
	parent,
	project_id,
	role_exists,
	role_missing_from_registry,
	subpath(full_path, -1) as full_path,
	parent_changed,
	approved,
	role_new,
	role_disposed,
	asset_id,
	asset_serial_number,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	joined_role_asset
where
nlevel(full_path) > 1 and role_exists = true and role_disposed = true;
!!!
create or replace
view general_unassigned_asset_view as
select
	asset_id as id,
	asset_serial_number,
	project_id,
	designer_planned_action_type_tbl_id,
	role_changed,
	role_link,
	installation_stage_id,
	uninstallation_stage_id,
	asset_exists,
	asset_new,
    asset_missing_from_registry
from
	base_asset_view
where
	role_link is null
    and designer_planned_action_type_tbl_id <> 'b' -- or this one
	and asset_exists = true; --might not want this filters