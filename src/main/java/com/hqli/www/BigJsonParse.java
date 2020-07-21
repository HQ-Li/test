package com.hqli.www;

import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.JSONReader;
import com.sun.istack.internal.NotNull;

import java.io.StringReader;
import java.util.LinkedList;
import java.util.List;

public class BigJsonParse<T> {


    public BigJsonParse(@NotNull String file){

    }

    List<T> getBean(String jsonStr){
        byte[] bytes = new byte[1024];
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(bytes);
        //bytes
        StringReader stringReader = new StringReader(jsonStr);

        JSONReader jsonReader = new JSONReader(stringReader);

        jsonReader.startArray();
        while (jsonReader.hasNext()){

            jsonReader.startObject();
            jsonReader.readObject();

        }
        jsonReader.endArray();
        jsonReader.close();

        return null ;
    }
}
