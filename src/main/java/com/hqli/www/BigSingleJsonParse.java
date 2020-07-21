package com.hqli.www;


import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;

import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.LinkedList;


public  class BigSingleJsonParse {
    Reader in = null;

    int count = 100000;

    ArrayList<SqlBean>  objectList = new ArrayList<SqlBean>();

    public BigSingleJsonParse(Reader in) {
        this.in = in;
    }

    public void readMessageArrayToDo(){
        if (in != null) {
            JsonReader reader = new JsonReader(in);
            try {
                reader.beginArray();
                while (reader.hasNext()) {
                    objectList.add(readMessage(reader));
                }
                reader.endArray();
                //toDoSome(objectList);
                objectList.clear();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }else{
            System.out.println("文件流传入为null。");
        }
    }

    public void readMessageArrayToDo(Reader in){
        this.in = in;
        readMessageArrayToDo();
    }

    public SqlBean readMessage(JsonReader reader){
        SqlBean sqlDat = new SqlBean();
        LinkedList lstRow = new LinkedList();
        try {
            //读取一个 sql 对象
            //对每一个对象， 要求字段的顺序性。 sql--> type -- > data (最后一个字段是 data)
            reader.beginObject();
            while (reader.hasNext()){
                String name = reader.nextName();
                //String sql = "";
                //读取sql字段
                if(name.equals("sql")){
                    String sql = reader.nextString();
                    sqlDat.setSql(sql);
                    System.out.println(sql);
                }else if(name.equals("type")){
                    //读取type字段
                    LinkedList lstType = new LinkedList();
                    reader.beginArray();
                    while (reader.hasNext()){
                        String typeValue = reader.nextString();
                        lstType.add(typeValue);
                    }
                    reader.endArray();
                    sqlDat.setLstType(lstType);
                    System.out.println(lstType.toString());
                }else if(name.equals("data")){
                    //读取data 字段 . 多行， 每行有多列
                    //LinkedList lstRow = new LinkedList();
                    reader.beginArray();

                    while (reader.hasNext()){
                        //读取每一行数据. 这里可能存在非常多行数据
                        LinkedList row = new LinkedList();
                        reader.beginArray();
                        while(reader.hasNext()){
                            final JsonToken token = reader.peek();
                            String rowValue;

                            switch ( token ) {
                                case NUMBER:
                                    rowValue = String.format("%s", reader.nextDouble() );
                                    break;
                                case STRING:
                                    rowValue = reader.nextString();
                                    break;
                                default:
                                      throw new AssertionError(token);
                            }
                            //每行有多列。 读取每一列的数据

                            row.add(rowValue);
                        }

                        reader.endArray();

                        lstRow.add(row);

                        //如果 多于10 万行， 则插入数据库
                        if(lstRow.size() > 100000){
                            sqlDat.setData(lstRow);
                            handleData(sqlDat);
                            lstRow.clear();
                        }
                    }

                    reader.endArray();
                }

            }

            if(lstRow.size() > 0){
                sqlDat.setData(lstRow);
                handleData(sqlDat);
                lstRow.clear();
            }

            reader.endObject();
        }catch (Exception e){
            e.printStackTrace();
        }

        return sqlDat;
    }

//    public void toDoSome(SqlBean objectList){
//
//    }

    boolean handleData(SqlBean objectList){

        for(LinkedList<String> row :objectList.getData()){
            System.out.println(row.toString());
        }
        System.out.println("==============");
        return true;
    }




}
