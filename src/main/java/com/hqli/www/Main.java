package com.hqli.www;

import java.io.FileReader;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1){
            System.out.println("[error] input file is empty:");
            return ;
        }

        String filePath = args[0];

        System.out.println("file path :" + filePath );
        try {
            BigSingleJsonParse parse = new BigSingleJsonParse(new FileReader(filePath));
            parse.readMessageArrayToDo();
            System.out.println("end.................");
        }catch (Exception e){
            e.printStackTrace();
        }

    }
}
