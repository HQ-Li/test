-- 如果存储过程存在就删除
DROP PROCEDURE IF EXISTS updateColumn;
CREATE PROCEDURE updateColumn()
BEGIN
-- 定义循环条件
DECLARE flag INT DEFAULT 0;
-- 保存表名
DECLARE tname VARCHAR(50);
-- 查询数据库sens_blog中含有del_flag列的表,如果区分大小写使用binary COLUMN_NAME = 'del_flag'
DECLARE result CURSOR FOR SELECT TABLE_NAME FROM  INFORMATION_SCHEMA.Columns WHERE TABLE_SCHEMA = 'sens_blog' AND  COLUMN_NAME = 'del_flag';
-- 退出循环
DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET flag = 1;
-- 打开游标
OPEN result;
    WHILE flag <> 1 DO
    -- 游标指向下一个位置,可以有多个数据,比如FETCH result INTO tname,ttype,...;
    FETCH result INTO tname;
        -- 拼接字符串表名sql,根据需要使用CONCAT函数连接
        -- 批量设置所有表的为del_flag字段0
        -- SET @execSql = CONCAT('UPDATE ', tname, ' SET del_flag = 0'); 
                -- 批量设置所有表的为del_flag字段默认值为0
                SET @execSql = CONCAT('ALTER TABLE  ', tname, ' ALTER COLUMN del_flag SET DEFAULT  0');
        PREPARE stmt FROM @execSql;
        EXECUTE stmt;
    END WHILE;
END;
-- 调用存储过程更新数据
CALL updateColumn();