-- ========================= CREATE Images TABLE =============================
CREATE TABLE
    images (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        url VARCHAR(2048) NOT NULL,
        metadata JSONB NULL,
        created_at TIMESTAMP
        WITH
            TIME ZONE NULL DEFAULT NOW ()
    ) TABLESPACE pg_default;

ALTER TABLE images ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON images AS PERMISSIVE FOR ALL TO public USING (true);