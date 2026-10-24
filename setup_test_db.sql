-- ============================================================================
-- Script: setup_test_db.sql
-- Description: Provision 4 synthetic vulnerable MySQL accounts for automated
--              ITGC audit testing and security outlier extraction (CAAT).
-- ============================================================================

CREATE USER IF NOT EXISTS 'test_admin'@'localhost' IDENTIFIED BY 'Password123!';
GRANT ALL PRIVILEGES ON *.* TO 'test_admin'@'localhost' WITH GRANT OPTION;

CREATE USER IF NOT EXISTS 'test_remote'@'%' IDENTIFIED BY 'Password123!';
GRANT SELECT ON *.* TO 'test_remote'@'%';

CREATE USER IF NOT EXISTS 'test_nopass'@'localhost' IDENTIFIED BY '';

CREATE USER IF NOT EXISTS ''@'localhost';

FLUSH PRIVILEGES;

-- ----------------------------------------------------------------------------
-- Cleanup / Reset Script (Uncomment and execute below to reset environment):
-- ----------------------------------------------------------------------------
-- DROP USER IF EXISTS 'test_admin'@'localhost';
-- DROP USER IF EXISTS 'test_remote'@'%';
-- DROP USER IF EXISTS 'test_nopass'@'localhost';
-- DROP USER IF EXISTS ''@'localhost';
-- FLUSH PRIVILEGES;

-- ----------------------------------------------------------------------------
-- Cleanup / Reset Script (Uncomment and execute below to reset environment):
-- ----------------------------------------------------------------------------
-- DROP USER IF EXISTS 'test_admin'@'localhost';
-- DROP USER IF EXISTS 'test_remote'@'%';
-- DROP USER IF EXISTS 'test_nopass'@'localhost';
-- DROP USER IF EXISTS ''@'localhost';
-- FLUSH PRIVILEGES;

