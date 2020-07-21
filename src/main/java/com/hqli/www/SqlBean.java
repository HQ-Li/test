package com.hqli.www;

import java.util.ArrayList;
import java.util.LinkedList;

public class SqlBean {
    String sql;
    LinkedList<String> lstType;
    LinkedList<LinkedList<String> > data;

    public void setLstType(LinkedList<String> lstType) {
        this.lstType = lstType;
    }

    public LinkedList<String> getLstType() {
        return lstType;
    }

    public String getSql() {
        return sql;
    }

    public void setSql(String sql) {
        this.sql = sql;
    }

    public void setData(LinkedList<LinkedList<String>> data) {
        this.data = data;
    }

    public LinkedList<LinkedList<String>> getData() {
        return data;
    }
}
