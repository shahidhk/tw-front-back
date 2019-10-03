create or replace view reconciliation_view as
select 
r.id, r.updatable_role_number as role_number,
r.role_name as role_name,
r.parent_id_id as parent,
r.project_tbl_id as project_id,
r.entity_exists as role_exists,
r.missing_from_registry as role_missing_from_registry,
r.ltree_path as full_path,
a.id as asset_id,
a.asset_serial_number as asset_serial_number,
a.entity_exists as asset_exists,
a.missing_from_registry as asset_missing_from_registry
from (
public."djangoAPI_ProjectAssetRoleRecordTbl" as br
right join public."djangoAPI_PreDesignReconciledRoleRecordTbl" as pr
on (br.id=pr.projectassetrolerecordtbl_ptr_id)) as r
left join (
public."djangoAPI_PreDesignReconciledAssetRecordTbl" as pa 
left join public."djangoAPI_ProjectAssetRecordTbl" as ba 
on (pa.projectassetrecordtbl_ptr_id=ba.id)) as a 
on (r.id=a.initial_project_asset_role_id_id)
;

create or replace view unassigned_assets as
select ba.id as id, ba.asset_serial_number as asset_serial_number
from public."djangoAPI_PreDesignReconciledAssetRecordTbl" as pa
left join public."djangoAPI_ProjectAssetRecordTbl" as ba
on pa.projectassetrecordtbl_ptr_id=ba.id
where pa.initial_project_asset_role_id_id is null and pa.designer_planned_action_type_tbl_id<>2
;

-- To impliment ltree
-- https://coderwall.com/p/whf3-a/hierarchical-data-in-postgres
add a ltree column to the role asset table
CREATE EXTENSION ltree;
CREATE INDEX parent_id_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" USING GIST (ltree_path);
CREATE INDEX parent_path_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" (parent_id_id);

CREATE OR REPLACE FUNCTION update_parent_path() RETURNS TRIGGER AS $$
    DECLARE
        path ltree;
    BEGIN
        IF NEW.parent_id_id IS NULL THEN
            NEW.ltree_path = 'root'::ltree;
        ELSEIF TG_OP = 'INSERT' OR OLD.parent_id_id IS NULL OR OLD.parent_id_id != NEW.parent_id_id THEN
            SELECT ltree_path || id::text FROM public."djangoAPI_ProjectAssetRoleRecordTbl" WHERE id = NEW.parent_id_id INTO path;
            IF path IS NULL THEN
                RAISE EXCEPTION 'Invalid parent_id %. Entities must be added parents first', NEW.parent_id_id;
            END IF;
            NEW.ltree_path = path;
            UPDATE public."djangoAPI_ProjectAssetRoleRecordTbl"
                SET ltree_path = path || subpath(ltree_path,nlevel(OLD.ltree_path)) WHERE ltree_path <@ OLD.ltree_path AND ltree_path != OLD.ltree_path;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER parent_path_tgr
    BEFORE INSERT OR UPDATE ON public."djangoAPI_ProjectAssetRoleRecordTbl"
    FOR EACH ROW EXECUTE PROCEDURE update_parent_path();