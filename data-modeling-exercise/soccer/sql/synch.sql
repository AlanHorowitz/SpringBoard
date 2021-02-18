-- MySQL Workbench Synchronization
-- Generated: 2021-02-18 17:47
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: alan

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

ALTER TABLE `soccer`.`Players` 
DROP FOREIGN KEY `fk_team_name`;

ALTER TABLE `soccer`.`Matches` 
DROP FOREIGN KEY `fk_home_team`,
DROP FOREIGN KEY `fk_visiting_team`;

ALTER TABLE `soccer`.`Goals` 
DROP FOREIGN KEY `fk_Goals_1`;

ALTER TABLE `soccer`.`Referees_has_Matches` 
DROP FOREIGN KEY `fk_Referees_has_Matches_Matches1`;

ALTER TABLE `soccer`.`Match_Results` 
DROP FOREIGN KEY `fk_match_id`,
DROP FOREIGN KEY `fk_team_id`;

ALTER TABLE `soccer`.`Players` 
ADD CONSTRAINT `fk_team_name`
  FOREIGN KEY (`team_name`)
  REFERENCES `soccer`.`Teams` (`team_name`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `soccer`.`Matches` 
ADD CONSTRAINT `fk_home_team`
  FOREIGN KEY (`home_team`)
  REFERENCES `soccer`.`Teams` (`team_name`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_visiting_team`
  FOREIGN KEY (`visiting_team`)
  REFERENCES `soccer`.`Teams` (`team_name`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `soccer`.`Goals` 
DROP FOREIGN KEY `fk_Goals_Players1`;

ALTER TABLE `soccer`.`Goals` ADD CONSTRAINT `fk_Goals_Players1`
  FOREIGN KEY (`player_id`)
  REFERENCES `soccer`.`Players` (`player_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_Goals_1`
  FOREIGN KEY (`match_id`)
  REFERENCES `soccer`.`Matches` (`match_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `soccer`.`Referees_has_Matches` 
DROP FOREIGN KEY `fk_Referees_has_Matches_Referees1`;

ALTER TABLE `soccer`.`Referees_has_Matches` ADD CONSTRAINT `fk_Referees_has_Matches_Referees1`
  FOREIGN KEY (`referee_id`)
  REFERENCES `soccer`.`Referees` (`referee_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_Referees_has_Matches_Matches1`
  FOREIGN KEY (`match_id`)
  REFERENCES `soccer`.`Matches` (`match_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `soccer`.`Match_Results` 
ADD CONSTRAINT `fk_match_id`
  FOREIGN KEY (`match_id`)
  REFERENCES `soccer`.`Matches` (`match_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_team_id`
  FOREIGN KEY (`team_name`)
  REFERENCES `soccer`.`Teams` (`team_name`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
