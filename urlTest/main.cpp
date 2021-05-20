#include "mainwindow.h"
#include <QApplication>
#include "testcallurl.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    TestCallUrl test;
    test.test();
    test.test2();


    return a.exec();
}
